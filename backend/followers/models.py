from asyncio import constants
from email.policy import default
from django.db import models
import uuid

# Create your models here.
from author.models import Author

#class Followers(models.Model):
#    author = models.ForeignKey(Author, on_delete = models.CASCADE)
#    type = models.TextField(default='followers')
#    object = models.URLField()


class FollowRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(default='Follow', max_length=6, editable=False)
    summary = models.CharField(max_length=100)
    # the author making the follow request
    actor = models.ForeignKey(Author, related_name = 'sent_follow_request', on_delete = models.CASCADE, default ='')
    # the author recieving the follow request
    object = models.ForeignKey(Author, related_name = 'recieved_follow_request', on_delete = models.CASCADE, default ='')

    class Meta:
        # only allows one follow request from a author to another author
        constraints = [models.UniqueConstraint(fields=['actor','object'],name='unique_friend_request')]