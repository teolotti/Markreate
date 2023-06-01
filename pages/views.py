from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404

from .forms import CreateServiceForm, EditServiceForm, ContactForm, PaymentForm, OrderForm, CompleteOrderForm
from .models import Service, Order


# Create your views here.

def home(request):
    services = Service.objects.all()
    context = {'services': services}
    return render(request, 'home.html', context)


def contact(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Your message has been sent successfully.')
    context = {'form': form}
    return render(request, 'contact.html', context)


@login_required(login_url='login')
def yourServices(request):
    if request.user.groups.filter(name='Sellers Group').exists():
        services = Service.objects.filter(seller=request.user.seller)
        context = {'services': services}
        return render(request, 'accounts/yourServices.html', context)
    else:
        return redirect('BecomeSeller')


@login_required(login_url='login')
def yourOrders(request):
    orders = Order.objects.filter(customer=request.user.customer)
    context = {'orders': orders}
    return render(request, 'accounts/yourOrders.html', context)


@login_required(login_url='login')
def create_service(request):
    if not request.user.groups.filter(name='Sellers Group').exists():
        return redirect('BecomeSeller')
    else:
        form = CreateServiceForm()

    if request.method == 'POST':
        form = CreateServiceForm(request.POST, request.FILES)
        if form.is_valid():
            service = form.save(commit=False)
            service.seller = request.user.seller
            service.save()
            return redirect('yourServices')
    context = {'form': form}
    return render(request, 'accounts/service_form.html', context)


@login_required(login_url='login')
def edit_service(request, id):
    if not request.user.groups.filter(name='Sellers Group').exists():
        return redirect('BecomeSeller')
    else:
        form = EditServiceForm()

    service = get_object_or_404(Service, id=id)

    if request.method == 'GET':
        context = {'form': EditServiceForm(instance=service), 'id': id}
        return render(request, 'accounts/service_form.html', context)

    if request.method == 'POST':
        form = EditServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            service = form.save(commit=False)
            service.save()
            messages.success(request, 'The post has been updated successfully.')
            return redirect('yourServices')
    context = {'form': form}
    return render(request, 'accounts/service_form.html', context)


@login_required(login_url='login')
def delete_service(request, id):
    service = get_object_or_404(Service, id=id)
    service.delete()
    messages.success(request, 'The post has been deleted successfully.')
    return redirect('yourServices')


def service(request, id):
    service = get_object_or_404(Service, id=id)
    seller = service.seller.user
    context = {'service': service, 'seller': seller}
    return render(request, 'service.html', context)


@login_required(login_url='login')
def order(request, id):
    service = get_object_or_404(Service, id=id)
    if request.user == service.seller.user:
        messages.warning(request, 'You cannot order your own service.')
        return redirect('home')
    form = PaymentForm()
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your order has been placed successfully.')
            Order.objects.create(service=service, customer=request.user.customer, PaymentCard=form.instance,
                                 date_ordered=datetime.today(), completed=False, file=None)
            return redirect('home')
    context = {'form': form, 'service': service}
    return render(request, 'order.html', context)


@login_required(login_url='login')
def orders_rec(request):
    if not request.user.groups.filter(name='Sellers Group').exists():
        return redirect('BecomeSeller')
    else:
        orders = Order.objects.filter(service__seller=request.user.seller)
        context = {'orders': orders}
        return render(request, 'accounts/orders_rec.html', context)


@login_required(login_url='login')
def complete_order(request, id):
    order = get_object_or_404(Order, id=id)
    if not request.user.seller == order.service.seller:
        messages.warning(request, 'You cannot complete this order.')
        return redirect('home')
    else:

        form = CompleteOrderForm()
        if request.method == 'GET':
            context = {'form': CompleteOrderForm(instance=order), 'id': id}
            return render(request, 'accounts/complete_order.html', context)
        if request.method == 'POST':
            form = CompleteOrderForm(request.POST, request.FILES, instance=order)
            if form.is_valid():
                order = form.save(commit=False)
                order.completed = True
                order.save()
                messages.success(request, 'Order has been completed successfully.')
                return redirect('orders_rec')
        context = {'form': form}
        return render(request, 'accounts/complete_order.html', context)
