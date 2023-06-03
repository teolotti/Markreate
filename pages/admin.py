from django.contrib import admin
from .models import Service, Order, PaymentCard, Review

# Register your models here.

admin.site.register(Service)
admin.site.register(Order)
admin.site.register(PaymentCard)
admin.site.register(Review)
