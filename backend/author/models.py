from django.db import models
from django.contrib.auth.models import User
import uuid

class Author(models.Model):
    # The user can be null for remote authors
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)

    # The type of the author, is always "author"
    type = models.CharField(max_length=6, default="author", editable=False)

    # The id of the author, is a UUID
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # The url to the author's profile
    url = models.URLField(blank=True, null=True, editable=False)

    # The host home of the author
    host = models.URLField(blank=True, null=True, editable=False)

    displayName = models.CharField(max_length=100, blank=True, null=True)

    # The github url of the author
    github = models.URLField(blank=True, null=True)

    # The profile image of the author
    profileImage = models.URLField(blank=True, null=True)

    # People that the author follows
    followers = models.ManyToManyField("self", related_name="following", symmetrical=False, blank=True)

    def compute_url(self):
        return f"{self.host}/authors/{self.id}"

    def save(self, *args, **kwargs):
        self.url = self.compute_url()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.displayName} - {self.id}"

