"""Contains the urls for the follower app."""

from django.conf.urls import include
from django.urls import path

from .views import FollowerList, FollowerDetail

urlpatterns = [
    path('', FollowerList.as_view(), name='follower-list'),
    path('<uuid:foreign_id>', FollowerDetail.as_view(), name='follower-detail'),
]