"""Contains the models for the node app."""

from django.db import models


class Node(models.Model):
    host = models.URLField(primary_key=True)    # includes backslash
    # We send this Basic auth info with every request to the node,
    # and also use it when this node sends us a request. That is, same username and password!
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    is_connected = models.BooleanField(default=True)

    def __str__(self):
        return f"Node is connected: {self.is_connected} at {self.host}"

    def save(self, *args, **kwargs):
        # We want to make sure that the host ends with a backslash
        if not self.host.endswith("/"):
            self.host += "/"
        super().save(*args, **kwargs)


"""To be deleted:
Team1:
username: team1
password: team4andteam1

Team2:
username: team2
password: team4andteam2

Team3:
username: team3
password: team4andteam3
"""
