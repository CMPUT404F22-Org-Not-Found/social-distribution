"""Contains the views for the follower app."""

from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from author.models import Author
from author.serializers import AuthorSerializer


class FollowerList(APIView):
    """List all the followers of a given author."""

    def get(self, request: Request, author_id: str, format: str = None) -> Response:
        """Return a list of all followers of a given author."""
        author = self.get_author(author_id)
        followers = list(author.followers.all())
        serializer = AuthorSerializer(followers, many=True)
        followers_response = {
            "type": "followers",
            "items": serializer.data,
        }
        return Response(followers_response, status=status.HTTP_200_OK)

    def get_author(self, pk: str) -> Author:
        """Return an author instance."""
        try:
            return Author.objects.get(pk=pk)
        except Author.DoesNotExist:
            raise Http404


class FollowerDetail(APIView):
    """Check if foreign author is following, or put as follower, or delete as follower."""

    def get(self, request: Request, author_id: str, foreign_id: str, format: str = None) -> Response:
        """Return a boolean indicating if the foreign author is following the given author."""
        author = self.get_author(author_id)
        foreign_author = self.get_author(foreign_id)
        is_following = foreign_author in author.followers.all()

        if not is_following:
            return Response({"type": "follower",
                            "detail": "Foreign author is not following the author."},
                            status=status.HTTP_200_OK)

        follower_serializer = AuthorSerializer(foreign_author)
        follower_response = follower_serializer.data
        follower_response["type"] = "follower"
        return Response(follower_response, status=status.HTTP_200_OK)

    def put(self, request: Request, author_id: str, foreign_id: str, format: str = None) -> Response:
        """Add the foreign author as a follower of the given author."""
        author = self.get_author(author_id)
        foreign_author = self.get_author(foreign_id)
        author.followers.add(foreign_author)
        response_dict = {"type": "follower",
                    "detail": f"Foreign author {foreign_author.displayName} "
                              f"is now following the author {author.displayName}."}
        return Response(response_dict, status=status.HTTP_200_OK)

    def delete(self, request: Request, author_id: str, foreign_id: str, format: str = None) -> Response:
        """Remove the foreign author as a follower of the given author."""
        author = self.get_author(author_id)
        foreign_author = self.get_author(foreign_id)
        author.followers.remove(foreign_author)
        response_dict = {"type": "follower",
                    "detail": f"Foreign author {foreign_author.displayName} "
                                f"is no longer following the author {author.displayName}."}
        return Response(response_dict, status=status.HTTP_200_OK)
    
    def get_author(self, pk: str) -> Author:
        """Return an author instance."""
        try:
            return Author.objects.get(pk=pk)
        except Author.DoesNotExist:
            raise Http404
