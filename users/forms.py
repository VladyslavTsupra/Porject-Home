from dataclasses import field

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm

from users.models import User


# User login form.
class UserLoginForm(AuthenticationForm):
    # Sets the form model and fields.
    class Meta:
        model = User
        fields = ("username", "password")

    username = forms.CharField()
    password = forms.CharField()


# New user registration form.
class UserRegistrationForm(UserCreationForm):
    # Sets the form model and fields.
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


# User profile edit form.
class ProfileForm(UserChangeForm):
    # Sets the form model and fields.
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
