from django.shortcuts import render
from accounts.forms import CreateCustomerForm


# Create your views here.

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
