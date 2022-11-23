"""Contains the views for the node app."""

from django.http import Http404
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


class NodeDetail(APIView):
    """Retrieve, update or delete a node instance."""

    def get_object(self, pk: str) -> Node:
        """Return the node instance."""
        try:
            return Node.objects.get(pk=pk)
        except Node.DoesNotExist:
            raise Http404

    def get(self, request: Request, pk: str, format: str = None) -> Response:
        """Return the node instance."""
        node = self.get_object(pk)
        serializer = NodeSerializer(node)
        return Response(serializer.data)

    def put(self, request: Request, pk: str, format: str = None) -> Response:
        """Update the node instance."""
        node = self.get_object(pk)
        serializer = NodeSerializer(node, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, pk: str, format: str = None) -> Response:
        """Delete the node instance."""
        node = self.get_object(pk)
        node.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
