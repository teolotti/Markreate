from django.forms import ModelForm
from django import forms

from pages.models import Order, Service


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = []


class CompleteOrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['file']


class CreateServiceForm(ModelForm):
    class Meta:
        model = Service
        fields = ['title', 'description', 'image', 'price']


class EditServiceForm(ModelForm):
    class Meta:
        model = Service
        fields = ['title', 'description', 'image', 'price']


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
