from re import T
from time import timezone
from django.db import models
from django.utils import timezone
from author.models import Author

import uuid
# Create your models here.

class Post(models.Model):

    CONTENT_CHOICE = [
        ("text/markdown","text/markdown"), 
        ("text/plain","text/plain"),
        ("application/base64","application/base64"),
        ("image/png;base64","image/png;base64"),
        ("image/jpeg;base64","image/jpeg;base64")
    ]

    VISIBILITY = [
        ("PUBLIC", "PUBLIC"),
        ("PRIVATE","PRIVATE")
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(default="post",max_length=4, editable=False)
    title = models.CharField(max_length=255,blank=True,null=True)
    source = models.URLField(max_length=500,null=True,blank=True)
    origin = models.URLField(max_length=500,null=True,blank=True)
    description = models.TextField(max_length=255, blank=True, null=True, default="")
    contentType = models.CharField(max_length=30, choices=CONTENT_CHOICE, default='text/plain')
    content = models.TextField(null=True, blank=True)
    author = models.ForeignKey(Author, related_name="post_author", on_delete=models.CASCADE)
    categories = models.TextField(default='[]', null=True)
    published = models.DateTimeField("Published",default=timezone.now)
    visibility = models.CharField(max_length=30, choices=VISIBILITY,default="PUBLIC")
    unlisted = models.BooleanField(default=False)
    comments = models.URLField(max_length=500,editable=False,null=True,blank=True)
    url = models.URLField(max_length=500,editable=False,null=True,blank=True)

    