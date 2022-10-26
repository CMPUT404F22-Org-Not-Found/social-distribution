"""Contains the urls for the like app."""

from django.conf.urls import include
from django.urls import path

from .views import LikedDetail,LikeDetail

urlpatterns = [
    path('', LikedDetail.as_view(), name='liked-detail'),

]