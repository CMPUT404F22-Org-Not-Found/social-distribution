"""Contains the models for the Inbox app."""

from django.db import models

from author.models import Author
from post.models import Post
from followers.models import FriendRequest


class Inbox(models.Model):
    type = models.CharField(max_length=5, default="inbox", editable=False)

    # The author who owns this inbox
    author = models.OneToOneField(Author, primary_key=True, related_name="inbox", on_delete=models.CASCADE)

    # The posts that are in this inbox
    posts = models.ManyToManyField(Post, related_name="inbox_post", blank=True, symmetrical=False)

    # The friend requests that are in this inbox
    friend_requests = models.ManyToManyField(FriendRequest, related_name="inbox_friend_request", blank=True, symmetrical=False)

    def __str__(self):
        return f"Inbox of {self.author.displayName} - {str(self.author.id)}"
