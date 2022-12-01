"""Contains request_verifiers for the inbox app.

This just make sures that in the request body,
the fields present are the ones that are in the
corresponding models; if not we delete the field.

The reason we need this is because we use get_or_create()
to create objects, and if the request body contains
fields that are not in the model, it will throw an error.
"""

import uuid

from author.models import Author
from post.models import Post
from followers.models import FriendRequest
from like.models import Like


def verify_author_request(request_body: dict) -> dict:
    """Verify the request body for author request."""
    author_fields = Author._meta.get_fields()
    author_field_names = [field.name for field in author_fields]
    keys_to_delete = []
    for key in request_body.keys():
        if key not in author_field_names:
            keys_to_delete.append(key)
    for key in keys_to_delete:
        del request_body[key]
    return request_body

def verify_post_request(request_body: dict) -> dict:
    """Verify the request body for post request."""
    post_fields = Post._meta.get_fields()
    post_field_names = [field.name for field in post_fields]
    keys_to_delete = []
    for key in request_body.keys():
        if key not in post_field_names:
            keys_to_delete.append(key)
    for key in keys_to_delete:
        del request_body[key]
    request_body["author"] = verify_author_request(request_body["author"])
    return request_body

def verify_friend_request(request_body: dict) -> dict:
    """Verify the request body for friend request."""
    friend_request_fields = FriendRequest._meta.get_fields()
    friend_request_field_names = [field.name for field in friend_request_fields]
    keys_to_delete = []
    for key in request_body.keys():
        if key not in friend_request_field_names:
            keys_to_delete.append(key)
    for key in keys_to_delete:
        del request_body[key]
    request_body["actor"] = verify_author_request(request_body["actor"])
    request_body["object"] = verify_author_request(request_body["object"])
    return request_body


def verify_like_request(request_body: dict) -> dict:
    """Verify the request body for like request."""
    like_fields = Like._meta.get_fields()
    like_field_names = [field.name for field in like_fields]
    keys_to_delete = []
    for key in request_body.keys():
        if key not in like_field_names:
            keys_to_delete.append(key)
    for key in keys_to_delete:
        del request_body[key]
    request_body["author"] = verify_author_request(request_body["author"])
    return request_body

def get_author_id_from_url(url: str) -> uuid:
    """Returns the author id from the url."""
    return uuid.UUID(url.split("/")[-1])
