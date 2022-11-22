"""Contains the urls for the node app."""

from django.urls import path
from .views import NodeList

urlpatterns = [
    path('', NodeList.as_view(), name="node-list"),
]
