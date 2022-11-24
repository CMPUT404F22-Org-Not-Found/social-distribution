"""socialdistribution URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from tempfile import template
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls import include
from django.urls import path
from author.views import Register, AuthorObject 
from post.views import PublicView
from rest_framework.authtoken import views as rest_framework_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('authors/', include('author.urls')),
    path('register/', Register.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('public/', PublicView.as_view(), name='public'),
    path('api-token-auth/', rest_framework_views.obtain_auth_token),
    path('author-object/',AuthorObject.as_view()),
    path('nodes/', include('node.urls')),
]
