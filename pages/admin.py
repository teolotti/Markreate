from django.contrib import admin
from .models import Service, Order, PaymentCard

# Register your models here.

admin.site.register(Service)
admin.site.register(Order)
admin.site.register(PaymentCard)
