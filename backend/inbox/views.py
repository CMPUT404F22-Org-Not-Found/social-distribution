"""Contains the views for the inbox app."""

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
            """When we POST a post to the inbox, if the post is already present, add the post to the inbox,
            if the post is not present, create a new post and add it to the inbox.
            """
            request_dict["author"] = author # we replace the json author with the author object
            post, was_post_created = Post.objects.get_or_create(id=request_dict.get("id", None),
                                                                defaults=request_dict)
            inbox.posts.add(post)
            inbox.save()
            if was_post_created:
                return Response({"type": "post",
                                 "detail": f"Successfully created a new post and sent to {author.displayName}'s inbox"},
                                 status=status.HTTP_201_CREATED)
            
            return Response({"type": "post",
                            "detail": f"Successfully sent the post to {author.displayName}'s inbox"},
                            status=status.HTTP_200_OK)

        elif request_dict["type"] == "follow":
            pass

        return Response(status=status.HTTP_200_OK)
