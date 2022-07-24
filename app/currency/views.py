from django.http import HttpResponse
from currency.models import Rate, ContactUs


def greeting(request):
    return HttpResponse('HELLO WORLD')


def rate_list(request):

    rate_list = []
    for rate in Rate.objects.all():
        html_string = f'ID: {rate.id}, sale: {rate.sale}, buy: {rate.buy} <br>'
        rate_list.append(html_string)
    return HttpResponse(str(rate_list))


def contactus(request):

    contactus_list = []
    for contact in ContactUs.objects.all():
        html_string = f'ID: {contact.id}, email_from: {contact.email_from}, email_to: {contact.email_to}, subject: {contact.subject} <br>'
        contactus_list.append(html_string)
    return HttpResponse(str(contactus_list))

