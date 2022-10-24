from ast import Delete
from django.http import Http404, HttpResponse

from .models import Post
from author.models import Author
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import PostSerializer
# Create your views here.

class PostList(APIView):

    def get(self,request,fk):
        try:
            Author.objects.get(pk=fk)
        except Author.DoesNotExist:
            raise Http404
        
        posts = Post.objects.all().order_by("published")
        serializer = PostSerializer(posts, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self,request,fk):
        try:
            Author.objects.get(pk=fk)
        except Author.DoesNotExist:
            raise Http404
        
        serializer = PostSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class PostDetail(APIView):

    def get_object(self,pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404


    def get_author(self,fk):
        try:
            Author.objects.get(pk=fk)
        except Author.DoesNotExist:
            raise Http404

    def get(self,request,pk,fk):
        try:
            post = self.get_object(pk=pk)
            serializer = PostSerializer(post)
            return Response(serializer.data, status= status.HTTP_200_OK)
        except Post.DoesNotExist:
            raise Http404

    def post(self,request,pk,fk):
        try:
            post = self.get_object(pk=pk)
            
        except Post.DoesNotExist:
            raise Http404
        serializer = PostSerializer(post,data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk,fk):
        try:
            post = self.get_object(pk=pk)
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Post.DoesNotExist:
            raise Http404

    def put(self, request, pk, fk):
        try:
            Author.objects.get(pk=fk)
        except Author.DoesNotExist:
            raise Http404

        try:
            Post.objects.get(pk=pk)
            return HttpResponse("Already Exists", status=status.HTTP_401_UNAUTHORIZED)
        except Post.DoesNotExist:
            post = self.get_object(pk=pk)
            serializer = PostSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, stauts=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)





