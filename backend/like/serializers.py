"""Contains the serializers for the Like app."""

from importlib.metadata import requires
from rest_framework import serializers

from author.serializers import AuthorSerializer
from .models import Like


class LikeSerializer(serializers.ModelSerializer):
    type = serializers.CharField(default="Like", read_only=True)
    author = AuthorSerializer(many=False, required=True)

    class Meta:
        model = Like
        fields = ['type', 'author', 'object', 'summary']
