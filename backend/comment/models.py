from time import timezone
from django.db import models
from django.utils import timezone
from author.models import Author
from post.models import Post

import uuid
# Create your models here.

class Comment(models.Model):

    CONTENT_CHOICE = [
        ("text/markdown","text/markdown"), 
        ("text/plain","text/plain"),
        ("application/base64","application/base64"),
        ("image/png;base64","image/png;base64"),
        ("image/jpeg;base64","image/jpeg;base64")
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(default="comment",max_length=7, editable=False)
    comment = models.TextField()
    contentType = models.CharField(max_length=30, choices=CONTENT_CHOICE, default='text/plain')
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    published = models.DateTimeField("Published",default=timezone.now)
    url = models.URLField(max_length=500,editable=False,null=True,blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_comment")
    
    def get_type(self):
        return self.contentType

    def get_id(self):
        return self.id
    
    def save(self, *args, **kwargs):
        self.url = str(self.post.url) + "/comments/" + str(self.id)
        super().save(*args, **kwargs)
