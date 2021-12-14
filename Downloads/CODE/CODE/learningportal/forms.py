from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from main.models import WebsiteUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = WebsiteUser
        fields = ('first_name', 'last_name', 'username', 'email')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = WebsiteUser
        fields = ('first_name', 'last_name', 'username', 'email')
