"""Contains the permissions for the author app."""
import re
from rest_framework import permissions

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
        
        try:

            request_uri = request.META['HTTP_REFERER']
            if DEFAULT_HOST.split('//')[1] in request_uri or "localhost" in request_uri:
                if "PostDetail" not in str(view) or request.method in permissions.SAFE_METHODS:
                    return True

                try:
                    author_id = request.user.author.id
                    uri = request.build_absolute_uri()
                except:
                    return False
                pattern = "[A-Za-z0-9]{8}-[A-Za-z0-9]{4}-[A-Za-z0-9]{4}-[A-Za-z0-9]{4}-[A-Za-z0-9]{12}"
                uuid = re.findall(pattern,uri)
                
                if len(uuid) > 0:
                    return uuid[0] == str(author_id)


        except:
            return False
            

