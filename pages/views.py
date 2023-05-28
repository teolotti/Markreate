from django.core.mail import send_mail
from django.shortcuts import render
from .models import Service


# Create your views here.

def home(request):
    services = Service.objects.all()
    context = {'services': services}
    return render(request, 'home.html', context)


def contact(request):
    if request.method == 'POST':
        # Gestisci i dati del modulo di contatto inviati
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
    return render(request, 'contact.html')