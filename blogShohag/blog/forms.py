from django import forms
from .models import Article,Author,Category
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CreateForm(forms.ModelForm):
    class Meta():
        model = Article
        fields = [
            'title',
            'body',
            'image',
            'category'

        ]


class CreateUser(UserCreationForm):
    class Meta():
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'

        ]


class CreateAuthor(forms.ModelForm):
    class Meta():
        model = Author
        fields = [
            'profile_picture',
            'details',

        ]


class CreateCategory(forms.ModelForm):
    class Meta():
        model = Category
        fields = [
            'name',

        ]
