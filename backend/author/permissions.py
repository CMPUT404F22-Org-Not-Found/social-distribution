"""Contains the permissions for the author app."""

from rest_framework import permissions


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


        