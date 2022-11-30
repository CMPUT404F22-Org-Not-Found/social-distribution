import uuid
import json
import requests, base64
from django.http import Http404, HttpResponse
from django.core.paginator import Paginator
from django.core.validators import URLValidator
from django.core.files.base import ContentFile
from .models import Post
from author.models import Author
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import PostSerializer
from author.permissions import IsAuthenticated, IsAuthorOrReadOnly
from rest_framework.renderers import BaseRenderer
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

        pid = uuid.uuid4()
        post_id = str(pid)
        post_id_url = author.url + "/posts/" + post_id
        request["id"] = post_id_url
        request["author"] = author

        if "categories" in request:
            request["categories"] = json.dumps(request["categories"])

        post, created = Post.objects.update_or_create(post_id=post_id, defaults=request)

        if created:
            send_post_to_inboxes(post, author)

        serializer = PostSerializer(post)

        # check if content type is image
        if serializer.validated_data.get("contentType").startswith("image"):
            image =  + pid.hex + "/image" # do we need request.build_absolute_uri()?
            serializer.validated_data["content"] = image # would probably need a image field if this doesn't work
            serializer = serializer.update(serializer,serializer.validated_data) # is this correct? if not use the code below
            '''
            serializer.save(
                id = post_id,
                title = 'Image Post',
                content = serializer.validated_data.get("content"),
                author = author,
                url = post_id_url,
            )
            '''
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

class ImagePostView(APIView):
    #renderer_classes = [ImageRenderer]

    #permission_classes = [IsAuthorOrReadOnly]

    def get(self, request, pk, post_id):

        try:
            author = self.get_author(pk)
            if author is None:
                raise Http404

            # need to check if authorized

            # get post obj
            post_obj = Post.objects.get(id=post_id, contentType__contains="image", visibility = "PUBLIC")

            if "base64" not in post_obj.content:
                validate = URLValidator()
                try:
                    validate(post_obj.content)
                    response = requests.get(post_obj.content)
                    if response.status_code == 200:
                        content_type = response.headers.get("content-type")
                        extension = content_type.split('/')[-1]
                        data = ContentFile(response.content, name='temp.'+extension)
                        return HttpResponse(data, content_type=content_type)
                except:
                    return Response("Content of this post is not a base64 encoded string", status=status.HTTP_400_BAD_REQUEST)

            # if 'base64' in post_obj.content, then decode the base64 into binary
            format, image_string = post_obj.content.split(';base64,')
            extension = format.split('/')[-1]
            data = ContentFile(base64.b64decode(image_string), name='temp.' + extension)

            return HttpResponse(data, content_type=f'image/{extension}')
        except Exception as e:
            return Response(f"Error: {e}", status=status.HTTP_400_BAD_REQUEST)

    def get_author(self,pk):
        try:
            author = Author.objects.get(pk=pk)
        except Author.DoesNotExist:
            return None
        return author    
