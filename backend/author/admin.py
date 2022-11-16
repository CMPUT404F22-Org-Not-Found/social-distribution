from django.contrib import admin
from .models import Author
from rest_framework.authtoken.admin import TokenAdmin

admin.site.register(Author)
TokenAdmin.raw_id_fields = ('user',)
