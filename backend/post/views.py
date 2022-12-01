import uuid
import json
from django.http import Http404
from django.core.paginator import Paginator
from .models import Post
from author.models import Author
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import PostSerializer
from author.permissions import IsAuthenticated, IsAuthorOrReadOnly

from node.node_connections import send_post_to_inboxes

class PublicView(APIView):
    def retrieve(self):
        try:
            return Post.objects.filter(visibility="PUBLIC").order_by('-published')
        except Post.DoesNotExist:
            return None
        
    def get(self,request):

        posts = list(self.retrieve())
        size = request.query_params.get("size",5)
        page = request.query_params.get("page",1)
        
        paginator = Paginator(posts,size)

        try:
            postsDisplay = paginator.page(page)
        except:
            postsDisplay = paginator.page(1)

        serializer = PostSerializer(postsDisplay,many=True)
        result = {
            "type": "public_posts", 
            "items": serializer.data
        }

        return Response(result,status=status.HTTP_200_OK)

class PostList(APIView):

    permission_classes = [IsAuthorOrReadOnly]

    def get_author(self,pk):
        try:
            author = Author.objects.get(pk=pk)
        except Author.DoesNotExist:
            return None
        return author

    def list(self,pk):
        try:
            return Post.objects.filter(author__author_id = pk,visibility = "PUBLIC", unlisted = False).order_by("-published")
        except Post.DoesNotExist:
            return None

    def get(self,request,pk):
        author = self.get_author(pk)
        if author is None:
            raise Http404

        posts = list(self.list(pk))
        size = request.query_params.get("size",5)
        page = request.query_params.get("page",1)
        
        paginator = Paginator(posts,size)

        try:
            postsDisplay = paginator.page(page)
        except:
            postsDisplay = paginator.page(1)
         
        serializer = PostSerializer(postsDisplay,many=True)
        result = {
            "type": "posts", 
            "items": serializer.data
        }

        return Response(result,status=status.HTTP_200_OK)

    def post(self,request,pk):

        author = self.get_author(pk)
        if author is None:
            raise Http404
        
        request = dict(request.data)

        post_id = str(uuid.uuid4())
        post_id_url = author.url + "/posts/" + post_id
        request["id"] = post_id_url
        request["author"] = author

        if "categories" in request:
            request["categories"] = json.dumps(request["categories"])

        post, created = Post.objects.update_or_create(post_id=post_id, defaults=request)

        if created:
            send_post_to_inboxes(post, author)

        serializer = PostSerializer(post)

        return Response(serializer.data, status = status.HTTP_201_CREATED)

class PostDetail(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self,author,post_id):
        try:
            return author.post_author.get(post_id=post_id)
        except Post.DoesNotExist:
            return None

    def get_author(self,pk):
        try:
            author = Author.objects.get(pk=pk)
        except Author.DoesNotExist:
            return None
        return author

    def get(self,request,pk,post_id):

        author = self.get_author(pk)
        if author is None:
            raise Http404

        post = self.get_object(author,post_id)
        if post is None:
            raise Http404
        serializer = PostSerializer(post)
        return Response(serializer.data,status=status.HTTP_200_OK)
        
    def post(self,request,pk,post_id):
        
        author = self.get_author(pk)
        if author is None:
            raise Http404
        
        request = dict(request.data)
        
        post = self.get_object(author,post_id)
        if post is None:
            raise Http404

        serializer = PostSerializer(post, data=request, partial=True)

        if serializer.is_valid():
            post = serializer.save()
            send_post_to_inboxes(post, author)

            if "categories" in request:
                post.categories = json.dumps(request["categories"])
                post.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request,pk,post_id):
        
        author = self.get_author(pk)
        if author is None:
            raise Http404

        post = self.get_object(author, post_id)
        if post is None:
            raise Http404
        post.delete()

        return Response("Deleted Successfully", status=status.HTTP_200_OK)

    def put(self, request, pk, post_id):
        
        author = self.get_author(pk)
        if author is None:
            raise Http404

        request = dict(request.data)

        post_id_url = author.url + "/posts/" + str(post_id)
        request["id"] = post_id_url
        request["author"] = author

        if "categories" in request:
                request["categories"] = json.dumps(request["categories"])

        post, created = Post.objects.update_or_create(post_id=post_id, defaults=request)
        if created:
            send_post_to_inboxes(post, author)
        serializer = PostSerializer(post)

        return Response(serializer.data, status = status.HTTP_201_CREATED)
        
