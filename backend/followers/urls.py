"""Contains the urls for the follower app."""

from django.conf.urls import include
from django.urls import path

from .views import FollowerList, FollowerDetail, FriendRequestList, FriendRequestDetail

urlpatterns = [
    path('', FollowerList.as_view(), name='follower-list'),
    path('<uuid:foreign_id>', FollowerDetail.as_view(), name='follower-detail'),
    path('friendrequest/', FriendRequestList.as_view(), name='friendrequest-list'),
    path('friendrequest/<uuid:foreign_id>', FriendRequestDetail.as_view(), name='friendrequest-detail'),
]