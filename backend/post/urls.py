from django.conf.urls import include
from django.urls import path

from .views import PostDetail, PostList, ImagePostView

urlpatterns = [
    path('',PostList.as_view(),name="post-list"),
    path('<uuid:post_id>/', PostDetail.as_view(),name="post-details"),
    path('<uuid:post_id>/comments/', include('comment.urls'), name="post-comments"),
    path('<uuid:post_id>/likes/', include('like.urls')),
    path('<uuid:post_id>/image/', ImagePostView.as_view(),name="image-details"),
]
