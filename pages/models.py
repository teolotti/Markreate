from django.db import models
from django.contrib.auth.models import AbstractUser
from accounts.models import Seller

# Create your models here.


class Service(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField()
    min_price = models.FloatField()
    seller = models.ForeignKey(Seller, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
