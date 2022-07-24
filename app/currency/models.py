from django.db import models


class Rate(models.Model):
    base_currency_type = models.CharField(max_length=5)
    currency_type = models.CharField(max_length=5)
    sale = models.DecimalField(max_digits=8, decimal_places=3)
    buy = models.DecimalField(max_digits=8, decimal_places=3)
    source = models.CharField(max_length=64)
    created = models.DateTimeField(auto_now_add=True)


class ContactUs(models.Model):
    email_from = models.EmailField()
    email_to = models.EmailField()
    subject = models.CharField(max_length=64)
    message = models.CharField(max_length=500)
