"""Contains the views for the inbox app."""

import uuid

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
from .models import Inbox


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

        posts_serializer = PostSerializer(posts_list, many=True)
        friend_requests_serializer = FriendRequestSerializer(friend_requests_list, many=True)

        response = {
            "type": "inbox",
            "author": str(author.url),
            "items": posts_serializer.data + friend_requests_serializer.data,
        }

        return Response(response, status=status.HTTP_200_OK)

    def post(self, request: Request, author_id: str, format: str = None) -> Response:
        """Send a post to the author.
            if the type is “post” then add that post to AUTHOR_IDs inbox
            if the type is “follow” then add that follow is added to AUTHOR_IDs inbox to approve later
            if the type is “like” then add that like to AUTHOR_IDs inbox
            if the type is “comment” then add that comment to AUTHOR_IDs inbox
        """
        try:
            author = Author.objects.get(pk=author_id)
        except Author.DoesNotExist:
            raise Http404("Author does not exist")

        try:
            inbox = Inbox.objects.get(author=author)
        except Inbox.DoesNotExist:
            raise Http404("Inbox does not exist")

        request_dict = request.data
        if request_dict["type"] == "post":
            return self._handle_POST_post(request_dict, author, inbox)

        elif request_dict["type"] == "follow":
            return self._handle_POST_follow(request_dict, author, inbox)
        
        elif request_dict["type"] == "like":
            return self._handle_POST_like(request_dict, author, inbox)
            
        elif request_dict["type"] == "like":
            return self._handle_POST_like(request_dict, author, inbox)
            
        return Response(status=status.HTTP_200_OK)
    
    def _handle_POST_post(self, post_request_dict: Dict, author: Author, inbox: Inbox) -> Response:
        """When we POST a post to the inbox, if the post is already present, add the post to the inbox,
        if the post is not present, create a new post and add it to the inbox.
        """
        post_author_dict = post_request_dict["author"]
        post_author_dict["id"] = uuid.UUID(post_author_dict["id"])
        # We may need to create a new author for remote author posts
        post_author, _ = Author.objects.get_or_create(
            id=post_author_dict["id"], defaults=post_author_dict
        )
        post_request_dict["author"] = post_author # we replace the json author with the author object
        post, was_post_created = Post.objects.get_or_create(id=post_request_dict.get("id", None),
                                                            defaults=post_request_dict)
        inbox.posts.add(post)
        inbox.save()
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
        # The object in friend requests is the recipient of the friend request and 
        # the recipient Author should thus already exist in the database.
        # The actor in friend requests is the sender of the friend request and
        # the sender Author may exist if he is a local author or may not exist if he is a remote author,
        # in which case we create him.
        recipient_dict = follow_request_dict["object"]
        recipient_autor = Author.objects.get(id=recipient_dict["id"])
        follow_request_dict["object"] = recipient_autor
        sender_dict = follow_request_dict["actor"]
        sender_author, _ = Author.objects.get_or_create(id=sender_dict["id"], defaults=sender_dict)
        follow_request_dict["actor"] = sender_author

        follow_request, was_follow_request_created = FriendRequest.objects.get_or_create(
            actor=sender_author, object=recipient_autor, defaults=follow_request_dict
        )
        inbox.friend_requests.add(follow_request)
        inbox.save()
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
        like_author = Author.objects.get_or_create(id=like_request_dict["author"]["id"],
                                                   defaults=like_request_dict["author"])
        like_request_dict["author"] = like_author

        like, was_like_created = Like.objects.get_or_create(
            author=like_author, object=like_request_dict["object"], defaults=like_request_dict)
        
        inbox.likes.add(like)
        inbox.save()

        if was_like_created:
            return Response({"type": "like",
                                "detail": f"Successfully created a new like and sent to {author.displayName}'s inbox"},
                                status=status.HTTP_201_CREATED)

        return Response({"type": "like",
                        "detail": f"Successfully sent the like to {author.displayName}'s inbox"},
                        status=status.HTTP_200_OK)

    
    def _handle_POST_like(self, like_request_dict: Dict, author: Author, inbox: Inbox) -> Response:
        
        post_like_dict = like_request_dict["author"]
        post_like_dict["id"] = uuid.UUID(post_like_dict["id"])

        # complete

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
