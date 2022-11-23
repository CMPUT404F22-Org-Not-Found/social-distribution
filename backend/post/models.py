
from django.urls import reverse
from time import timezone
from django.db import models
from django.utils import timezone
from author.models import Author

DEFAULT_HOST = "http://127.0.0.1:8000/"

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

    post_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id = models.URLField(max_length=2048, blank=True, null=True, editable=False)
    type = models.CharField(default="post",max_length=4, editable=False)
    title = models.CharField(max_length=255,null=True)
    count = models.IntegerField(default=0,blank=True,null=True)
    source = models.URLField(max_length=500,default=DEFAULT_HOST)
    origin = models.URLField(max_length=500,default=DEFAULT_HOST)
    description = models.TextField(max_length=255, blank=True, null=True, default="")
    contentType = models.CharField(max_length=30, choices=CONTENT_CHOICE, default='text/plain')
    content = models.TextField(null=True, blank=True)
    author = models.ForeignKey(Author, related_name="post_author", on_delete=models.CASCADE)
    categories = models.TextField(default='[]', null=True)
    published = models.DateTimeField("Published",default=timezone.now)
    visibility = models.CharField(max_length=30, choices=VISIBILITY,default="PUBLIC")
    unlisted = models.BooleanField(default=False)
    url = models.URLField(max_length=500,editable=False,null=True)
    comments = models.URLField(max_length=500,editable=False,default=str(url) + '/comments')
    
    def get_type(self):
        return self.contentType
        
    def get_id(self):
        return self.id
        
    def get_source(self):
        return str(self.source) + 'posts/' + str(self.post_id)
    
    def get_origin(self):
        return str(self.origin) + 'posts/' + str(self.post_id)

    def get_comments(self):
        return str(self.author.url) + '/posts/' + str(self.post_id) + '/comments'
    
    def get_absolute_url(self):
        return reverse('post-details', args=[str(self.author.id),str(self.post_id)])

    def save(self, *args, **kwargs):
        self.url = str(self.author.url) + '/posts/' + str(self.post_id)
        self.id = self.url
        super().save(*args, **kwargs)