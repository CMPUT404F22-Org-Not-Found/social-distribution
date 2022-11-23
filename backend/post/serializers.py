from comment.serializers import CommentSerializer
from .models import Post
from rest_framework import serializers
from author.serializers import AuthorSerializer

import json

class PostSerializer(serializers.ModelSerializer):

    author = AuthorSerializer(read_only = False)
    type = serializers.CharField(default='post', read_only=True)
    id = serializers.URLField(source="get_id", read_only=True)
    contentType = serializers.CharField(source="get_type",required = False)
    comments = serializers.URLField(source="get_comments",required=False,read_only=True)
    source = serializers.URLField(source="get_source",required=False,read_only=True)
    origin = serializers.URLField(source="get_origin",required=False,read_only=True)
    categories = serializers.SerializerMethodField()
    commentsSrc = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ("id","type","title","source","origin","description","contentType","content","author","categories","count","comments","commentsSrc","published","visibility","unlisted","url")

    def create(self, validated_data):
        post = Post.objects.create(**validated_data)
        return post
    
    def update(self, instance, validated_data):
        
        instance.title = validated_data.get('title',instance.title)
        instance.description = validated_data.get('description',instance.description)
        instance.content = validated_data.get('content', instance.content)
        instance.visibility = validated_data.get('visibility', instance.visibility)
        instance.unlisted = validated_data.get('unlisted', instance.unlisted)
        instance.published = validated_data.get("published",instance.published)
        
        instance.save()

        return instance

    def get_commentsSrc(self,post):
        comments = list(post.post_comment.all())
        comments = CommentSerializer(comments,many=True).data
        commentsSrc = {
            "type": "comments",
            "post": post.get_id(),
            "id": post.get_comments(),
            "comments": comments
        }

        return commentsSrc
        
    def get_categories(self, post):
        try:
            categories = json.loads(post.categories)
        except:
            categories = []
        
        return categories

    def get_count(self,post):
        return len(list(post.post_comment.all()))