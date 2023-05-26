from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from accounts.models import Customer
from django import forms


class CreateCustomerForm(UserCreationForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class LoginCustomerForm(AuthenticationForm):
    class Meta:
        model = Customer
        fields = ['username', 'password']