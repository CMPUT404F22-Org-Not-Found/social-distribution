from django.conf.urls import include
from django.urls import path

from .views import PostDetail
from like.views import LikeDetail

urlpatterns = [
    path('',PostDetail.as_view()),
    path('<uuid:post_id>/', PostDetail.as_view()),
    path('<uuid:post_id>/likes', LikeDetail.as_view()),
]