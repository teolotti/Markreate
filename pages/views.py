from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404

from .forms import CreateServiceForm, EditServiceForm, ContactForm, PaymentForm, OrderForm, CompleteOrderForm, \
    RatingForm
from .models import Service, Order, Review


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
    reviews = Review.objects.filter(service=service)
    context = {'service': service, 'seller': seller, 'reviews': reviews}
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


def search(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        services = Service.objects.filter(title__contains=searched)
        context = {'searched': searched, 'services': services}
        return render(request, 'search_home.html', context)


def order_by_price(request):
    ord_services = Service.objects.all().order_by('price')
    context = {'services': ord_services}
    return render(request, 'home.html', context)


@login_required(login_url='login')
def rate(request, id):
    service = get_object_or_404(Service, id=id)
    if Order.objects.filter(customer=request.user.customer, completed=True, service=service).exists():
        form = RatingForm()
    else:
        messages.warning(request, 'You cannot rate this service.')
        return redirect('yourOrders')
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.service = service
            review.customer = request.user.customer
            review.date = datetime.today()
            review.save()
            messages.success(request, 'Your rating has been submitted successfully.')
            return redirect('yourOrders')
    context = {'form': form, 'service': service}
    return render(request, 'accounts/rate.html', context)


def view_profile(request, id):
    profile = get_object_or_404(User, id=id)
    if request.user == profile:
        return redirect('profile')
    if profile.groups.filter(name='Sellers Group').exists():
        services = Service.objects.filter(seller=profile.seller)
        context = {'profile': profile, 'services': services}
        return render(request, 'profile_view.html', context)
    else:
        context = {'profile': profile}
        return render(request, 'profile_view.html', context)
