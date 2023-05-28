from django.db import models
from django.contrib.auth.models import AbstractUser
from accounts.models import Seller


# Create your models here.


class Service(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField()
    price = models.FloatField()
    seller = models.ForeignKey(Seller, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Order(models.Model):
    customer = models.ForeignKey('accounts.Customer', default=None, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, default=None, on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    file = models.FileField(default=None, blank=True, null=True)

    def __str__(self):
        return self.customer.user.username + ' - ' + self.service.title
