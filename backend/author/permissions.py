"""Contains the permissions for the author app."""
from rest_framework import permissions
from post.models import Post

DEFAULT_HOST = "http://127.0.0.1:8000"

class IsAuthorOrReadOnly(permissions.BasePermission):
    """Custom permission to allow only authors to edit their own profile."""

    def has_permission(self, request, view) -> bool:
        """Returns True if user logged in is the author, False otherwise."""
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # # if it'is a post method, check if the user is the author
        # if request.method == "POST":
        #     return request.user.is_authenticated and request.user.author.id == view.kwargs["pk"]
        
        return request.user.is_authenticated and request.user.author.id == view.kwargs["pk"]


class IsAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
            
        if request.method in permissions.SAFE_METHODS:
            return True
        try:

            post_id = view.kwargs["post_id"]
            post = Post.objects.get(id=post_id)
            return request.user.is_authenticated and (request.user.author.id == post.author.id)
            
        except:
            pass
        