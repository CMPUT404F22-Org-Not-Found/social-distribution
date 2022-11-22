
from comment.serializers import CommentSerializer
from django.http import Http404
from rest_framework.views import APIView
from author.models import Author
from post.models import Post
from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework import status
from .models import Comment
import uuid

class CommentDetail(APIView):

    def get_author(self,pk):
        try:
            author = Author.objects.get(pk=pk)
        except Author.DoesNotExist:
            return None
        return author

    def get_post(self,author,post_id):
        try:
            return author.post_author.get(id=post_id)
        except Post.DoesNotExist:
            return None
    
    def get_comment(self,post,comment_id):
        try:
            return post.post_comment.get(id=comment_id)
        except Comment.DoesNotExist:
            return None

    def get(self,request,pk,post_id,comment_id = None):
        author = self.get_author(pk)

        if author is None:
            raise Http404
        
        
        post = self.get_post(author,post_id)
        if post is None:
            raise Http404

        if comment_id is None:
            comments = list(post.post_comment.all())

            size = request.query_params.get("size",5)
            page = request.query_params.get("page",1)

            paginator = Paginator(comments,size)

            try:
                commentsDisplay = paginator.page(page)
            except:
                commentsDisplay = paginator.page(1)
            
            serializer = CommentSerializer(commentsDisplay,many=True)
            result = {
                "type": "comments",
                "page": page,
                "size": len(serializer.data),
                "post": str(post.url),
                "comments": serializer.data
            }

            return Response(result, status=status.HTTP_200_OK)

        comment = self.get_comment(post,comment_id)

        if comment is None:
            raise Http404

        serializer = CommentSerializer(comment)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self,request,pk,post_id):

        author = self.get_author(pk)

        if author is None:
            raise Http404

        post = self.get_post(author,post_id)
        if post is None:
            raise Http404
        
        request = dict(request.data)
        request["post"] = post
        request["id"] = str(uuid.uuid4())
        author_data = request["author"]
        if author_data is None:
            request["author"] = author
        else:
            author = self.get_author(pk = author_data["id"].split("/")[-1])
            request["author"] = author 

        comment, created = Comment.objects.update_or_create(id=request["id"], defaults=request)

        serializer = CommentSerializer(comment)

        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
