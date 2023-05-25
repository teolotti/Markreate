from django.shortcuts import render
from .models import Service


# Create your views here.

def home(request):
    services = Service.objects.all()
    return render(request, 'home.html', {'services': services})
