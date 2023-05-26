from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class Customer(AbstractUser):
    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
        ordering = ['id']


class Seller(Customer):
    profile_pic = models.ImageField(default='default.jpg', upload_to='profile_pics')
    profession = models.CharField(max_length=200, default=None, blank=True, null=True)
    personal_info = models.TextField(default=None, blank=True, null=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Seller'
        verbose_name_plural = 'Sellers'
        ordering = ['id']
