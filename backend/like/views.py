from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from author.models import Author
from post.models import Post
from .models import Like

from .serializers import LikeSerializer
from author.permissions import IsAuthorOrReadOnly

# Create your views here.


class LikeDetail(APIView):
    """Retrieves details about a like object"""

    #permission_classes = [IsAuthorOrReadOnly]

    # do we need post? like obejct sent in inbox

    def get(self, request, author_id, post_id, comment_id = None):
        """Retrieves likes a post or comment has"""
        
        author = self.get_author(author_id)
        post = self.get_post(post_id)
        
        # implement comments
        #if comment_id == None:
        #    raise Http404

        likes_on_post = list(Like.objects.filter(object=post.url))
        likes_on_post = LikeSerializer(likes_on_post, many=True)
        likes_response = {"type":"Likes","items":likes_on_post.data}
        Response(likes_response)

    def get_author(self, pk: str) -> Author:
        """Return an author instance."""
        try:
            return Author.objects.get(pk=pk)
        except Author.DoesNotExist:
            raise Http404

    def get_post(self, pk: str) -> Post:
        """Return an post instance."""
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

class LikedDetail(APIView):
    """Retrieves details about a liked object"""
    #permission_classes = [IsAuthorOrReadOnly] do we need authentication here

    def get(self, request, author_id):
        '''gets all public posts the author has liked'''
        author = self.get_author(author_id)
        posts_liked = list(Post.objects.get(author=author)) # is this correct
        posts_liked = LikeSerializer(posts_liked, many=True)
        liked_response = {"type":"Liked","items":posts_liked.data}
        return Response(liked_response)

    def get_author(self, pk: str) -> Author:
        """Return an author instance."""
        try:
            return Author.objects.get(pk=pk)
        except Author.DoesNotExist:
            raise Http404
