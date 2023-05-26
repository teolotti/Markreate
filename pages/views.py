from django.shortcuts import render
from .models import Service
from .forms import CreateCustomerForm
from django.contrib.auth.forms import UserCreationForm


# Create your views here.

def home(request):
    services = Service.objects.all()
    context = {'services': services}
    return render(request, 'home.html', context)


def loginPage(request):
    form = CreateCustomerForm()

    context = {'form': form}
    return render(request, 'accounts/login.html', context)


def registerPage(request):
    form = CreateCustomerForm()

    if request.method == 'POST':
        form = CreateCustomerForm(request.POST)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'accounts/registration.html', context)
