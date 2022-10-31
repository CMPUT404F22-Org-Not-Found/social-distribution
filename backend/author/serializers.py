"""Serializers for the author app."""

from rest_framework.serializers import ModelSerializer
from .models import Author

class AuthorSerializer(ModelSerializer):
    """Serializer for the Author model."""

    class Meta:
        model = Author
        fields = ("type", "id", "url", "host", "displayName", "github", "profileImage")

