"""Contains the views for the author app."""

import logging

from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import exceptions
from django.contrib.auth import authenticate
import datetime
from inbox.models import Inbox
from .models import Author
from .serializers import AuthorSerializer
from .permissions import IsAuthorOrReadOnly
from .forms import RegisterForm

from node.models import Node
from node.node_connections import update_db_with_global_authors

logger = logging.getLogger(__name__)


class AuthorList(APIView):
    """List all authors, or create a new author."""
    _DEFUALT_PAGE_SIZE = 10
    _DEFAULT_PAGE_NUM = 1

    def get(self, request: Request, format: str = None) -> Response:
        """Return a list of all authors."""
        authors = self._get_paginated_authors(request)
        serializer = AuthorSerializer(authors, many=True)
        response = {"type": "authors", "items": serializer.data}
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request: Request, format: str = None) -> Response:
        """Create a new author."""
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def _get_paginated_authors(self, request: Request) -> Paginator:
        """Return a paginated list of authors."""
        get_global_authors = request.query_params.get("global", False)
        if get_global_authors:
            update_db_with_global_authors()
        authors = Author.objects.all()
        page_size = request.query_params.get("size", self._DEFUALT_PAGE_SIZE)
        page_num = request.query_params.get("page", self._DEFAULT_PAGE_NUM)
        paginator = Paginator(authors, page_size)
        return paginator.get_page(page_num)


class AuthorDetail(APIView):
    """Retrieve, update or delete an author instance."""
    permission_classes = [IsAuthorOrReadOnly]

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
        """Updates the author instance."""
        author = self.get_object(pk)
        serializer = AuthorSerializer(author, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, pk: str, format: str = None) -> Response:
        """Delete an author instance."""
        author = self.get_object(pk)
        author.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Register(APIView):
    """Register a new author."""
    permission_classes = [AllowAny]
    def post(self, request: Request, format: str = None) -> Response:
        """Creates a new author."""
        form = RegisterForm(request.data)
        if form.is_valid():
            user = form.save()
            displayName = form.cleaned_data.get("displayName")
            github = form.cleaned_data.get("github")
            profileImage = form.cleaned_data.get("profileImage")
            author = Author.objects.create(user=user, displayName=displayName, github=github,
                        profileImage=profileImage, host=request.build_absolute_uri('/'))
            Inbox.objects.create(author=author)
            return redirect('login')
            # return Response(status=status.HTTP_201_CREATED)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request: Request, format: str = None) -> Response:
        """Return a form to register a new author."""
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})


class AuthorObject(APIView):
    def post(self,request: Request, format: str=None, *args, **kwargs):

        username = request.data["username"]
        password = request.data["password"]
        user = authenticate(None, username = username, password = password, **kwargs)
        if user is not None:
            token, created =  Token.objects.get_or_create(user=user)
            if not created:
                # update the created time of the token to keep it valid
                token.created = datetime.datetime.utcnow()
                token.save()
        else:
            raise exceptions.AuthenticationFailed('No such user')

        author = Author.objects.get(user=user)
        serializer = AuthorSerializer(author)
        serialized_author = serializer.data

        response = {"token" : token.key, "author": serialized_author}
        return Response(response,status=status.HTTP_200_OK)
