from django.db import models
from currency.model_choices import CURRENCY_TYPES


class Rate(models.Model):
    base_currency_type = models.CharField(max_length=5, choices=CURRENCY_TYPES)
    currency_type = models.CharField(max_length=5, choices=CURRENCY_TYPES)
    sale = models.DecimalField(max_digits=8, decimal_places=3)
    buy = models.DecimalField(max_digits=8, decimal_places=3)
    source = models.ForeignKey('currency.Source', on_delete=models.CASCADE, null=True, default=None)
    created = models.DateTimeField(auto_now_add=True)


class ContactUs(models.Model):
    email_from = models.EmailField()
    email_to = models.EmailField()
    subject = models.CharField(max_length=64)
    message = models.CharField(max_length=500)


def source_logo(instance, filename):
    return 'logo/{0}/{1}'.format(instance.id, filename)


class Source(models.Model):
    source_url = models.CharField(max_length=255)
    name = models.CharField(max_length=64)
    code_name = models.CharField(max_length=16, unique=True)
    logo = models.FileField(upload_to=source_logo)


class ResponseLog(models.Model):
    response_time = models.FloatField()
    request_method = models.CharField(max_length=6)
    query_params = models.CharField(max_length=124)
    ip = models.CharField(max_length=124)
    path = models.CharField(max_length=124)
