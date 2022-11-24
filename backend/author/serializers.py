"""Serializers for the author app."""

from rest_framework.serializers import ModelSerializer
from .models import Author

class AuthorSerializer(ModelSerializer):
    """Serializer for the Author model."""

    class Meta:
        model = Author
        fields = ("type", "id", "url", "host", "displayName", "github", "profileImage")

    def create(self, validated_data):
        """Create a new author."""
        # We get the author_id from the id, by splitting the url
        author_id = validated_data["id"].split("/")[-1]
        validated_data["author_id"] = author_id
        return Author.objects.create(**validated_data)
