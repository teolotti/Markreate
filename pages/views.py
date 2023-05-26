from django.shortcuts import render
from .models import Service



# Create your views here.

def home(request):
    services = Service.objects.all()
    context = {'services': services}
    return render(request, 'home.html', context)



