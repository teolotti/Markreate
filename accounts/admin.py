from django.contrib import admin
from .models import Customer
from .models import Seller


# Register your models here.
admin.site.register(Customer)
admin.site.register(Seller)