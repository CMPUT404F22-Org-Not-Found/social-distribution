from django.conf.urls import include
from django.urls import path
from .views import AuthorList, AuthorDetail


urlpatterns = [
    path('', AuthorList.as_view()),
    path('<uuid:pk>', AuthorDetail.as_view()),
]
