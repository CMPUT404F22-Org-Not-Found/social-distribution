from django.urls import path
from like.views import LikeView

from .views import CommentDetail
urlpatterns = [
    path('', CommentDetail.as_view(),name="comment-list"),
    path('<uuid:comment_id>', CommentDetail.as_view(),name="comment-detail"),
    path('<uuid:comment_id>/likes', LikeView.as_view(),name="like-detail")
]

