"""Contains the models for the Like app."""

from django.db import models

from author.models import Author


class Like(models.Model):
    type = models.CharField(max_length=5, default="Like", editable=False)

    # The author who liked the object
    author = models.ForeignKey(Author, related_name="like_author", on_delete=models.CASCADE)

    # The object that was liked
    object = models.URLField(max_length=500, editable=False)

    summary = models.CharField(max_length=500)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['author','object'], name="unique_like")
        ]
    
    def __str__(self):
        return f"{self.author.displayName} liked {self.object}"
