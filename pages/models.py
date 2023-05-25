from django.db import models


# Create your models here.

class Service(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField()
    min_price = models.FloatField()

    def __str__(self):
        return self.title
