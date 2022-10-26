"""Contains the views for the follower app."""

from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from author.models import Author
from django.http import Http404
from author.serializers import AuthorSerializer

from .models import FriendRequest
from .serializers import FriendRequestSerializer


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


class FriendRequestList(APIView):
    """List all the friend requests of a given author."""

    def get(self, request: Request, author_id: str, format: str = None) -> Response:
        """Return a list of all friend requests recieved by the given author."""
        author = self.get_author(author_id)
        friend_requests = list(author.recieved_friend_request.all())
        serializer = FriendRequestSerializer(friend_requests, many=True)
        friend_requests_response = {
            "type": "friendRequestsRecieved",
            "items": serializer.data,
        }
        return Response(friend_requests_response, status=status.HTTP_200_OK)

    def get_author(self, pk: str) -> Author:
        """Return an author instance."""
        try:
            return Author.objects.get(pk=pk)
        except Author.DoesNotExist:
            raise Http404

    
class FriendRequestDetail(APIView):
    """Check if foreign author has requested to be freinds with author,
        or put as adding a friend request, or delete as removing a friend request."""

    def get(self, request: Request, author_id: str, foreign_id: str, format: str = None) -> Response:
        """Return a boolean indicating if the author has a pending friend request with the foreign author."""
        author = self.get_author(author_id)
        foreign_author = self.get_author(foreign_id)
        friend_request = FriendRequest.objects.filter(actor=author, object=foreign_author)
        if not friend_request:
            return Response({"type": "friendRequest",
                            "detail": "Author has no pending friend request for the foreign author."},
                            status=status.HTTP_200_OK)
        
        friend_request_serializer = FriendRequestSerializer(friend_request[0])
        friend_request_response = friend_request_serializer.data
        friend_request_response["type"] = "friendRequest"
        return Response(friend_request_response, status=status.HTTP_200_OK)

    def post(self, request: Request, author_id: str, foreign_id: str, format: str = None) -> Response:
        """Add a friend request from the author to the foreign author."""
        author = self.get_author(author_id)
        foreign_author = self.get_author(foreign_id)
        friend_request = FriendRequest.objects.create(
            type="Follow", summary=f"{author.displayName} wants to be follow  {foreign_author.displayName}",
            actor=author, object=foreign_author)
        friend_request.save()

        response_dict = {"type": "friendRequest",
                    "detail": f"Author {author.displayName} has sent a friend request to the foreign author {foreign_author.displayName}."}
        return Response(response_dict, status=status.HTTP_200_OK)

    def delete(self, request: Request, author_id: str, foreign_id: str, format: str = None) -> Response:
        """Remove the friend request from the author to the foreign author."""
        author = self.get_author(author_id)
        foreign_author = self.get_author(foreign_id)
        friend_request = FriendRequest.objects.filter(actor=author, object=foreign_author)
        friend_request.delete()

        response_dict = {"type": "friendRequest",
                    "detail": f"Author {author.displayName} has removed the friend request to the foreign author {foreign_author.displayName}."}
        return Response(response_dict, status=status.HTTP_200_OK)
    
    def get_author(self, pk: str) -> Author:
        """Return an author instance."""
        try:
            return Author.objects.get(pk=pk)
        except Author.DoesNotExist:
            raise Http404
