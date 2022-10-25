from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    displayName = forms.CharField(max_length=100, required=True, help_text="Required")
    github = forms.URLField(max_length=200, required=False, help_text="Optional")
    profileImage = forms.URLField(max_length=200, required=False, help_text="Optional")

    class Meta:
        model = User
        fields = ("username", "displayName", "github", "profileImage")
