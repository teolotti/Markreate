from django.contrib.auth.models import User, Group
from django.db import models


# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'


class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    profile_pic = models.ImageField(upload_to='profile_pics')
    profession = models.CharField(max_length=200, default=None, blank=True, null=True)
    personal_info = models.TextField(default=None, blank=True, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Seller'
        verbose_name_plural = 'Sellers'
