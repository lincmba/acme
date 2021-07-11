from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    """
    Model representing a single product
    """
    sku = models.CharField(unique=True, max_length=100)
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True)
    active = models.BooleanField(blank=True, null=True)
    date_created = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)




class Webhook(models.Model):
    """
    Model representing webhooks implementation
    """
    name = models.CharField(max_length=100)
    url = models.URLField()
    date_created = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)
    active = models.BooleanField(default=True, blank=False, null=False)
