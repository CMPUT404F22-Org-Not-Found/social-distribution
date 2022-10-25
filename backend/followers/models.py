"""Contains the models for the follower app."""

from django.db import models
import uuid
from author.models import Author


class FriendRequest(models.Model):
    # The id of the friend request
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # The type of the friend request: constant
    type = models.CharField(default='Follow', max_length=6, editable=False)

    # The summary of the friend request
    summary = models.CharField(max_length=100)

    # The author making the friend request
    actor = models.ForeignKey(Author, related_name = 'sent_friend_request', on_delete = models.CASCADE, default ='')

    # The author recieving the friend request
    object = models.ForeignKey(Author, related_name = 'recieved_friend_request', on_delete = models.CASCADE, default ='')

    class Meta:
        # only allows one friend request from a author to another author
        constraints = [models.UniqueConstraint(fields=['actor','object'],name='unique_friend_request')]
