"""Contains the views for the Like app."""

from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from author.models import Author
from post.models import Post
from .models import Like
from .serializers import LikeSerializer


class LikeView(APIView):
    
    def get(self, request: Request, pk: str, post_id: str) -> Response:
        """Return the likes of the post."""
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            raise Http404("Post does not exist")


        likes = list(Like.objects.filter(object=post.url))
        likes = LikeSerializer(likes, many=True)
        likes_dict = {"type": "likes", "items": likes.data}
        return Response(likes_dict, status=status.HTTP_200_OK)           
