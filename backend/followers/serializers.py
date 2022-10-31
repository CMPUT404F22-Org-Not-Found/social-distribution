"""Contains the serializers for the follower app."""

from rest_framework import serializers
from .models import FriendRequest
from author.serializers import AuthorSerializer


class FriendRequestSerializer(serializers.ModelSerializer):
    """Serializer for the FriendRequest model."""
    actor = AuthorSerializer(many=False, required=True)
    object = AuthorSerializer(many=False, required=True)
    summary = serializers.CharField(max_length=100, required=False)

    class Meta:
        model = FriendRequest
        fields = ("type", "summary", "actor", "object")
