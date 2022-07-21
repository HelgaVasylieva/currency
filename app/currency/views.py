from django.http import HttpResponse


def greeting(request):
    return HttpResponse('HELLO WORLD')
