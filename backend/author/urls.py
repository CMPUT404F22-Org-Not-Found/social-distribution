from django.conf.urls import include
from django.urls import path
from .views import AuthorList, AuthorDetail

urlpatterns = [
    path('', AuthorList.as_view(), name="author-list"),
    path('<uuid:pk>/', AuthorDetail.as_view(), name="author-detail"),
    path('<uuid:pk>/posts/',include('post.urls'), name="author-posts"),
    path('<uuid:author_id>/followers/', include('followers.urls'), name="author-followers"),
    path('<uuid:author_id>/inbox/', include('inbox.urls'), name="author-inbox"),
    path('<uuid:author_id>/liked/', include('like.urls'), name="author-liked"), # is this correct
]

