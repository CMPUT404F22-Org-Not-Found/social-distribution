"""Contains the views for the inbox app."""

import uuid
import logging

from typing import Dict
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from author.models import Author
from author.serializers import AuthorSerializer
from post.models import Post
from post.serializers import PostSerializer
from followers.models import FriendRequest
from followers.serializers import FriendRequestSerializer
from like.models import Like
from like.serializers import LikeSerializer
from .models import Inbox
from .request_verifier import verify_author_request, verify_post_request, verify_friend_request, verify_like_request, get_author_id_from_url
from node.node_connections import is_local_author, send_friend_request_to_global_inbox, send_like_to_global_inbox, send_post_to_global_inbox

logger = logging.getLogger(__name__)

class InboxView(APIView):
    """The inbox view."""

    def get(self, request: Request, author_id: str, format: str = None) -> Response:
        """Return the inbox of the author, which icludes all the posts, friend requests sent to the author."""
        try:
            author = Author.objects.get(pk=author_id)
        except Author.DoesNotExist:
            raise Http404("Author does not exist")

        try:
            inbox = Inbox.objects.get(author=author)
        except Inbox.DoesNotExist:
            raise Http404("Inbox does not exist")

        posts_list = list(inbox.posts.all().order_by("-published"))
        friend_requests_list = list(inbox.friend_requests.all())
        likes_list = list(inbox.likes.all())

        posts_serializer = PostSerializer(posts_list, many=True)
        friend_requests_serializer = FriendRequestSerializer(friend_requests_list, many=True)
        likes_serializer = LikeSerializer(likes_list, many=True)

        response = {
            "type": "inbox",
            "author": str(author.url),
            "items": posts_serializer.data + friend_requests_serializer.data + likes_serializer.data,
        }

        return Response(response, status=status.HTTP_200_OK)

    def post(self, request: Request, author_id: str, format: str = None) -> Response:
        """Send a post to the author.
            if the type is ???post??? then add that post to AUTHOR_IDs inbox
            if the type is ???follow??? then add that follow is added to AUTHOR_IDs inbox to approve later
            if the type is ???like??? then add that like to AUTHOR_IDs inbox
            if the type is ???comment??? then add that comment to AUTHOR_IDs inbox
        """
        try:
            author = Author.objects.get(pk=author_id)
        except Author.DoesNotExist:
            raise Http404("Author does not exist")

        try:
            inbox, _ = Inbox.objects.get_or_create(author=author)
        except Inbox.DoesNotExist:
            raise Http404("Inbox does not exist")

        try:
            request_dict = request.data
            if request_dict["type"].lower() == "post":
                return self._handle_POST_post(request_dict, author, inbox)

            elif request_dict["type"].lower() == "follow":
                return self._handle_POST_follow(request_dict, author, inbox)
            
            elif request_dict["type"].lower() == "like":
                return self._handle_POST_like(request_dict, author, inbox)
        except Exception as e:
            logger.error(e)
            return Response({"type": "error",
                            "detail": "Error while sending the request to the inbox",
                            "exception": str(e),},
                            status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"type": "error",
                        "detail": "The type of the request is not supported"},
                        status=status.HTTP_400_BAD_REQUEST)

    
    def _handle_POST_post(self, post_request_dict: Dict, author: Author, inbox: Inbox) -> Response:
        """When we POST a post to the inbox, if the post is already present, add the post to the inbox,
        if the post is not present, create a new post and add it to the inbox.
        """
        post_request_dict = verify_post_request(post_request_dict)
        post_author_dict = post_request_dict["author"]
        # The id given is a url, so we need to extract the id from the url
        post_author_id = get_author_id_from_url(post_author_dict["id"])
        # We may need to create a new author for remote author posts
        post_author, _ = Author.objects.get_or_create(
            author_id=post_author_id, defaults=post_author_dict
        )
        post_request_dict["author"] = post_author # we replace the json author with the author object
        post_id = get_post_id_from_url(post_request_dict.get("id", f"a/{uuid.uuid4()}"))
        post, was_post_created = Post.objects.get_or_create(post_id=post_id, defaults=post_request_dict)
        inbox.posts.add(post)
        inbox.save()

        if not is_local_author(author):
            send_post_to_global_inbox(post, author)

        if was_post_created:
            return Response({"type": "post",
                                "detail": f"Successfully created a new post and sent to {author.displayName}'s inbox"},
                                status=status.HTTP_201_CREATED)
        
        return Response({"type": "post",
                        "detail": f"Successfully sent the post to {author.displayName}'s inbox"},
                        status=status.HTTP_200_OK)

    def _handle_POST_follow(self, follow_request_dict: Dict, author: Author, inbox: Inbox) -> Response:
        """When we POST a follow request to the inbox, if the follow request is already present,
        add the follow request to the inbox,
        if the follow request is not present, create a new follow request and add it to the inbox.
        """
        follow_request_dict = verify_friend_request(follow_request_dict)
        # The object in friend requests is the recipient of the friend request and 
        # the recipient Author should thus already exist in the database.
        # The actor in friend requests is the sender of the friend request and
        # the sender Author may exist if he is a local author or may not exist if he is a remote author,
        # in which case we create him.
        recipient_dict = follow_request_dict["object"]
        recipient_author = Author.objects.get(author_id=get_author_id_from_url(recipient_dict["id"]))
        follow_request_dict["object"] = recipient_author
        sender_dict = follow_request_dict["actor"]
        sender_author, was_created = Author.objects.get_or_create(author_id=get_author_id_from_url(sender_dict["id"]), defaults=sender_dict)
        follow_request_dict["actor"] = sender_author

        follow_request, was_follow_request_created = FriendRequest.objects.get_or_create(
            actor=sender_author, object=recipient_author, defaults=follow_request_dict
        )
        inbox.friend_requests.add(follow_request)
        inbox.save()

        if not is_local_author(recipient_author):
            send_friend_request_to_global_inbox(follow_request, recipient_author)

        if was_follow_request_created:
            return Response({"type": "follow",
                                "detail": f"Successfully created a new follow request and sent to {author.displayName}'s inbox"},
                                status=status.HTTP_201_CREATED)
        
        return Response({"type": "follow",
                        "detail": f"Successfully sent the follow request to {author.displayName}'s inbox"},
                        status=status.HTTP_200_OK)

    def _handle_POST_like(self, like_request_dict: Dict, author: Author, inbox: Inbox) -> Response:
        """When a like object is sent to the inbox, if it is already in the DB, add it to the inbox,
        if it is not in the DB, create a new like object and add it to the inbox.
        If the author is a remote author, create a new author object for him.
        """
        like_request_dict = verify_like_request(like_request_dict)
        like_author, _ = Author.objects.get_or_create(
            author_id=get_author_id_from_url(like_request_dict["author"]["id"]),
            defaults=like_request_dict["author"])
        like_request_dict["author"] = like_author

        like, was_like_created = Like.objects.get_or_create(
            author=like_author, object=like_request_dict["object"], defaults=like_request_dict)
        inbox.likes.add(like)
        inbox.save()

        if not is_local_author(like_author):
            send_like_to_global_inbox(like, like_author)

        if was_like_created:
            return Response({"type": "like",
                                "detail": f"Successfully created a new like and sent to {author.displayName}'s inbox"},
                                status=status.HTTP_201_CREATED)

        return Response({"type": "like",
                        "detail": f"Successfully sent the like to {author.displayName}'s inbox"},
                        status=status.HTTP_200_OK)

    
    def delete(self, request: Request, author_id: str, format: str = None) -> Response:
        """Clears the inbox of the author."""
        try:
            author = Author.objects.get(pk=author_id)
        except Author.DoesNotExist:
            raise Http404("Author does not exist")

        try:
            inbox = Inbox.objects.get(author=author)
        except Inbox.DoesNotExist:
            raise Http404("Inbox does not exist")

        inbox.posts.clear()
        inbox.friend_requests.clear()
        inbox.save()

        response_dict = {
            "type": "inbox",
            "author": str(author.id),
            "detail": f"Successfully cleared {author.displayName}'s inbox",
        }
        return Response(response_dict, status=status.HTTP_204_NO_CONTENT)

def get_post_id_from_url(url: str) -> uuid:
    """Returns the post id from the url."""
    try:
        return uuid.UUID(url.split("/")[-1])
    except Exception:
        return None
