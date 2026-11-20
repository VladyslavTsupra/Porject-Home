from dataclasses import field

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm

from users.models import User


# Форма входу користувача.
class UserLoginForm(AuthenticationForm):
    # Задає модель і поля форми.
    class Meta:
        model = User
        fields = ("username", "password")

    username = forms.CharField()
    password = forms.CharField()


# Форма реєстрації нового користувача.
class UserRegistrationForm(UserCreationForm):
    # Задає модель і поля форми.
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        )

    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField()
    email = forms.CharField()
    password1 = forms.CharField()
    password2 = forms.CharField()


# Форма редагування профілю користувача.
class ProfileForm(UserChangeForm):
    # Задає модель і поля форми.
    class Meta:
        model = User
        fields = (
            "image",
            "first_name",
            "last_name",
            "username",
            "email",
        )

    image = forms.ImageField(required=False)
    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField()
    email = forms.CharField()
