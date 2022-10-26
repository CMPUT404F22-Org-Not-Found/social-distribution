"""Contains the serializers for the like app."""

from email.policy import default
from rest_framework import serializers
from author.serializers import AuthorSerializer
from .models import Like


class LikeSerializer(serializers.ModelSerializer):
    """Serializer for the FriendRequest model."""
    type = serializers.CharField(default='Like')
    author = AuthorSerializer(many=False, required=True)

    class Meta:
        model = Like
        fields = ("type", "summary", "author", "object")

# where do we keep the create method