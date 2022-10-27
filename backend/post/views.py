
from django import urls
from author.serializers import AuthorSerializer
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
# Create your views here.

class PostDetail(APIView):

    def get_object(self,author,post_id):
        try:
            return author.post_author.get(id=post_id)
        except Post.DoesNotExist:
            return None

    def list(self,pk):
        try:
            return Post.objects.filter(author__id = pk,visibility = "PUBLIC", unlisted = False).order_by("-published")
        except Post.DoesNotExist:
            return None

    def get_author(self,pk):
        try:
            author = Author.objects.get(pk=pk)
        except Author.DoesNotExist:
            return None
        return author

    def get(self,request,pk,post_id = None):

        author = self.get_author(pk)
        if author is None:
            raise Http404

        if post_id is not None:
            post = self.get_object(author,post_id)
            if post is None:
                raise Http404
            serializer = PostSerializer(post)
            return Response(serializer.data,status=status.HTTP_200_OK)
        
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

    def post(self,request,pk,post_id = None):

        author = self.get_author(pk)
        if author is None:
            raise Http404
        
        request = dict(request.data)

        if post_id is not None:

            post = self.get_object(author,post_id)
            if post is None:
                raise Http404

            serializer = PostSerializer(post, data=request, partial=True)

            if serializer.is_valid():
                post = serializer.save()

                if "categories" in request:
                    post.categories = json.dumps(request["categories"])
                    post.save()

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        request["id"] = str(uuid.uuid4())
        request["author"] = author

        if "categories" in request:
            request["categories"] = json.dumps(request["categories"])

        post, created = Post.objects.update_or_create(id=request["id"], defaults=request)
        serializer = PostSerializer(post)

        return Response(serializer.data, status = status.HTTP_201_CREATED)
       

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
        request["id"] = post_id
        request["author"] = author

        if "categories" in request:
                request["categories"] = json.dumps(request["categories"])

        post, created = Post.objects.update_or_create(id=post_id, defaults=request)
        serializer = PostSerializer(post)

        return Response(serializer.data, status = status.HTTP_201_CREATED)
        


        

        

        
        






