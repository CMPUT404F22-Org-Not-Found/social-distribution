"""Contains the views for the author app."""

from django.http import Http404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from .models import Author
from .serializers import AuthorSerializer



class AuthorList(APIView):
    """List all authors, or create a new author."""

    def get(self, request: Request, format: str = None) -> Response:
        """Return a list of all authors."""
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data)

    def post(self, request: Request, format: str = None) -> Response:
        """Create a new author."""
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class AuthorDetail(APIView):
    """Retrieve, update or delete an author instance."""

    def get_object(self, pk: str) -> Author:
        """Return an author instance."""
        try:
            return Author.objects.get(pk=pk)
        except Author.DoesNotExist:
            raise Http404

    def get(self, request: Request, pk: str, format: str = None) -> Response:
        """Return an author instance."""
        author = self.get_object(pk)
        serializer = AuthorSerializer(author)
        return Response(serializer.data)

    def post(self, request: Request, pk: str, format: str = None) -> Response:
        """Return an error."""
        author = self.get_object(pk)
        serializer = AuthorSerializer(author)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, pk: str, format: str = None) -> Response:
        """Delete an author instance."""
        author = self.get_object(pk)
        author.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
