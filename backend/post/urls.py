from django.conf.urls import include
from django.urls import path

from .views import PostDetail

urlpatterns = [
    path('',PostDetail.as_view(),name="post-list"),
    path('<uuid:post_id>/', PostDetail.as_view(),name="post-details"),
    path('<uuid:post_id>/comments/', include('comment.urls'), name="post-comments"),
]

