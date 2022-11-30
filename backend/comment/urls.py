from django.conf.urls import include
from django.urls import path

from .views import CommentDetail
urlpatterns = [
    path('', CommentDetail.as_view(),name="comment-list"),
    path('<uuid:comment_id>', CommentDetail.as_view(),name="comment-detail"),
    path('<uuid:comment_id>/likes/', include('like.urls')),
]