from time import timezone
from django.db import models
from django.utils import timezone
from author.models import Author

import uuid
# Create your models here.

class Post(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(default="post",max_length=4, editable=False)
    title = models.CharField(max_length=255)
    source = models.URLField(blank=True,null=True)
    origin = models.URLField(blank=True,null=True)
    description = models.TextField()
    contentType = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(Author, related_name="post_author", on_delete=models.CASCADE)
    categories = models.TextField()
    published = models.DateTimeField(default=timezone.now)
    visibility = models.CharField(max_length=255)
    unlisted = models.BooleanField()
    comments = models.URLField(blank=True,null=True)
    count = models.PositiveBigIntegerField()