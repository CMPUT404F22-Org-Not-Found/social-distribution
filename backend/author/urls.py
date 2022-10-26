from django.conf.urls import include
from django.urls import path
from .views import AuthorList, AuthorDetail
from like.views import LikedView

urlpatterns = [
    path('', AuthorList.as_view(), name="author-list"),
    path('<uuid:pk>/', AuthorDetail.as_view(), name="author-detail"),
    path('<uuid:pk>/posts/',include('post.urls'), name="author-posts"),
    path('<uuid:author_id>/followers/', include('followers.urls'), name="author-followers"),
    path('<uuid:author_id>/inbox/', include('inbox.urls'), name="author-inbox"),
    path('<uuid:author_id>/liked/', LikedView.as_view(), name="author-liked"),
]

