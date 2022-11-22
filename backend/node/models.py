"""Contains the models for the node app."""

from django.db import models


class Node(models.Model):
    host = models.URLField(primary_key=True)    # doesnt include backslash
    # We send this Basic auth info with every request to the node,
    # and also use it when this node sends us a request. That is, same username and password!
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    is_connected = models.BooleanField(default=True)
