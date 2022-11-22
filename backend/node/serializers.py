"""Contsins the serializers for the node app."""

from rest_framework.serializers import ModelSerializer
from .models import Node


class NodeSerializer(ModelSerializer):
    """Serializer for the Node model."""

    class Meta:
        model = Node
        fields = ("host", "username", "password", "is_connected")
