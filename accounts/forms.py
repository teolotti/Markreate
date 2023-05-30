from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from accounts.models import User
from accounts.models import Seller
from django import forms


class CreateCustomerForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class LoginCustomerForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class BecomeSellerForm(ModelForm):
    class Meta:
        model = Seller
        fields = ['profile_pic', 'profession', 'personal_info']




