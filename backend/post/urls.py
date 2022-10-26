from django.conf.urls import include
from django.urls import path

from .views import PostDetail

urlpatterns = [
    path('',PostDetail.as_view()),
    path('<uuid:post_id>/', PostDetail.as_view()),
]