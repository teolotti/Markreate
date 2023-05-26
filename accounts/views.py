from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from accounts.forms import CreateCustomerForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


# Create your views here.

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                messages.success(request, 'Login effettuato con successo!')
                return redirect('home')
        else:
            messages.error(request, 'Username o password errati!')
            form = AuthenticationForm(request)
        context = {'form': form}
        return render(request, 'accounts/login.html', context)


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateCustomerForm()

        if request.method == 'POST':
            form = CreateCustomerForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Account creato con successo!')
                return redirect('login')

        context = {'form': form}
        return render(request, 'accounts/registration.html', context)


def logoutUser(request):
    logout(request)
    messages.success(request, 'Logout effettuato con successo!')
    return redirect('home')


@login_required(login_url='login')
def becomeSeller(request):
    form = CreateCustomerForm()

    context = {'form': form}
    return render(request, 'accounts/becomeSeller.html', context)
