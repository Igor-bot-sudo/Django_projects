from django.db import models


# Create your models here.

class Subscription(models.Model):
    rate_name = models.CharField(max_length=20)
    cost = models.FloatField()
