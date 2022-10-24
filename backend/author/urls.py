from django.conf.urls import include
from django.urls import path
from .views import AuthorList, AuthorDetail


urlpatterns = [
    path('', AuthorList.as_view(), name='author-list'),
    path('<uuid:pk>', AuthorDetail.as_view(), name='author-detail'),
]
