from .models import Post
from rest_framework import serializers
from author.serializers import AuthorSerializer

class PostSerializer(serializers.ModelSerializer):

    author = AuthorSerializer(read_only = False)

    class Meta:
        model = Post
        fields = ("id","type","title","source","origin","description","contentType","content","author","categories","comments","published","visibility","unlisted")

    def create(self, validated_data):
        return Post.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        
        instance.title = validated_data.get('title',instance.title)
        instance.description = validated_data.get('description',instance.description)
        instance.contentType = validated_data.get('contentType', instance.categories)
        instance.content = validated_data.get('content', instance.content)
        instance.visibility = validated_data.get('visibility', instance.visibility)
        instance.unlisted = validated_data.get('unlisted', instance.unlisted)
        instance.published = validated_data.get("published",instance.published)
        
        instance.save()

        return instance