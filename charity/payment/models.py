from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Order(models.Model):
    customer_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    total_cost = models.IntegerField()
    payment_method = models.CharField(max_length=255)
    is_paid = models.BooleanField(default=False)
