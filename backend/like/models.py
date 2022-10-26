"""Contains the models for the like app."""

from django.db import models
import uuid
from author.models import Author

class Like(models.Model):
    # The id of the Like object
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # The summary of the Like object
    summary = models.CharField(max_length=100)

    # The type of the Like: constant
    type = models.CharField(default='Like', max_length=4, editable=False)

    # The author creating the like object
    author = models.ForeignKey(Author, related_name = 'author_who_liked', on_delete = models.CASCADE, default ='')

    # url of the post including the author id of the author creating the like object and the id of the post liked
    object = models.URLField(blank=True, null=True, editable=False) # ??

    class Meta:
        # only allows one friend request from a author to another author
        constraints = [models.UniqueConstraint(fields=['author','object'],name='unique_like')]
