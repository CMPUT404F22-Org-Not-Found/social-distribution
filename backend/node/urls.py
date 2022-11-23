"""Contains the urls for the node app."""

from django.urls import path
from .views import NodeList, NodeDetail

urlpatterns = [
    path('', NodeList.as_view(), name="node-list"),
    path('<str:pk>/', NodeDetail.as_view(), name="node-detail"),
]
