from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.forms import PasswordInput
from .models import Images

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'username', 'placeholder': 'Username...', 'id': 'su-username'}),
            'email': forms.EmailInput(attrs={'class': 'email', 'placeholder': 'Email...', 'id': 'su-email'}),
            'first_name': forms.TextInput(attrs={'class': 'fn', 'placeholder': 'First name...', 'id': 'su-fn'}),
            'last_name': forms.TextInput(attrs={'class': 'ln', 'placeholder': 'Last name...', 'id': 'su-ln'}),
        }

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        self.fields['password1'].widget = PasswordInput(attrs={
            'class': 'password1',
            'placeholder': 'Password...',
            'id': 'su-password1'})

        self.fields['password2'].widget = PasswordInput(attrs={
            'class': 'password2',
            'placeholder': 'Confirm password...',
            'id': 'su-password2'})
