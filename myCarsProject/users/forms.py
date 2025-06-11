# users/forms.py

from django import forms
from django.contrib.auth.forms import AuthenticationForm

class EmailOrUsernameAuthenticationForm(AuthenticationForm):
    """
    Форма логина: в одном поле пользователь вводит либо e-mail, либо username.
    """
    username = forms.CharField(
        label='E-mail или логин',
        widget=forms.TextInput(attrs={'autofocus': True})
    )
