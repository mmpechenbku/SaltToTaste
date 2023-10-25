from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import TextInput

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('avatar', 'name', 'nickname', 'email')
        #
        # widgets = {
        #     "name" : TextInput(attrs={
        #         'class' :
        #     })
        # }


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')
