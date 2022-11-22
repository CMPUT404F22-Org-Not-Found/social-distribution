"""Contains the views for the node app."""

from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from .models import Node
from .serializers import NodeSerializer


class NodeList(APIView):
    """List all nodes, or create a new node."""

    def get(self, request: Request, format: str = None) -> Response:
        """Return a list of all nodes."""
        nodes = Node.objects.all()
        serializer = NodeSerializer(nodes, many=True)
        return Response(serializer.data)

    def post(self, request: Request, format: str = None) -> Response:
        """Create a new node."""
        serializer = NodeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
