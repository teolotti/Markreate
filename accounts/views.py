from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from django.db.transaction import commit
from django.shortcuts import render, redirect
from accounts.forms import CreateCustomerForm, LoginCustomerForm, BecomeSellerForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from accounts.models import Customer


# Create your views here.

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            form = LoginCustomerForm(request, data=request.POST)  # auth form
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                messages.success(request, 'Login effettuato con successo!')
                return redirect('home')
        else:
            messages.error(request, 'Username o password errati!')
            form = LoginCustomerForm(request)
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
                user = form.save(commit=False)
                user.is_customer = True
                if commit:
                    user.save()
                Customer.objects.create(user=user)
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
    if request.user.groups.filter(name='Sellers Group').exists():
        return redirect('home')
    else:
        form = BecomeSellerForm()

    if request.method == 'POST':
        form = BecomeSellerForm(request.POST)
        if form.is_valid():
            seller = form.save(commit=False)
            seller.user = request.user
            group = Group.objects.get(name='Sellers Group')
            group.user_set.add(seller.user)
            if commit:
                seller.save()
            messages.success(request, 'Sei diventato un venditore!')
            return redirect('home')

    context = {'form': form}
    return render(request, 'accounts/becomeSeller.html', context)
