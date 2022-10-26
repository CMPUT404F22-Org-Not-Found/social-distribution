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
            raise Http404

        inbox = Inbox.objects.get(author=author)

        posts_list = list(inbox.posts.all().order_by("-published"))
        friend_requests_list = list(inbox.friend_requests.all())

        posts_serializer = PostSerializer(posts_list, many=True)
        friend_requests_serializer = FriendRequestSerializer(friend_requests_list, many=True)

        response = {
            "type": "inbox",
            "author": str(author.url),
            "items": [posts_serializer.data + friend_requests_serializer.data],
        }

        return Response(response, status=status.HTTP_200_OK)
