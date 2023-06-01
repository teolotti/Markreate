import mimetypes

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from django.db.transaction import commit
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from Markreate.settings import BASE_DIR, MEDIA_ROOT
from accounts.forms import CreateCustomerForm, LoginCustomerForm, BecomeSellerForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from accounts.models import Customer
from pages.models import Service, Order


# Create your views here.

def loginPage(request):
    form = LoginCustomerForm()
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
        form = BecomeSellerForm(request.POST, request.FILES)
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


@login_required(login_url='login')
def profile(request):
    orders = Order.objects.filter(customer=request.user.customer)
    context = {'orders': orders}
    return render(request, 'accounts/profile.html', context)


@login_required(login_url='login')
def edit_profile(request):
    form1 = None
    form2 = None
    if request.user.groups.filter(name='Sellers Group').exists():
        seller = request.user.seller
        if request.method == 'GET':
            context = {'form1': CreateCustomerForm(instance=seller.user), 'form2': BecomeSellerForm(instance=seller),
                       'seller': seller}
            return render(request, 'accounts/edit_profile.html', context)
        if request.method == 'POST':
            form1 = BecomeSellerForm(request.POST, request.FILES, instance=seller)
            form2 = CreateCustomerForm(request.POST, instance=seller.user)
            if form1.is_valid() and form2.is_valid():
                form1.save()
                form2.save()
                messages.success(request, 'Profilo aggiornato con successo!')
                return redirect('profile')
    else:
        customer = request.user.customer
        if request.method == 'GET':
            context = {'form1': CreateCustomerForm(instance=customer.user), 'form2': None, 'customer': customer}
            return render(request, 'accounts/edit_profile.html', context)
        if request.method == 'POST':
            form = CreateCustomerForm(request.POST, instance=customer)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profilo aggiornato con successo!')
                return redirect('profile')
    context = {'form1': form1, 'form2': form2}
    return render(request, 'accounts/edit_profile.html', context)


def download(request, id): # FIXME: download file
    order = get_object_or_404(Order, id=id)
    filename = order.file.name
    filepath = MEDIA_ROOT + '/' + filename
    path = open(filepath, 'r')
    mime_type, _ = mimetypes.guess_type(filepath)
    response = HttpResponse(path, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response

