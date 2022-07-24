from django.contrib import admin
from django.urls import path

from currency.views import greeting, rate_list, contactus

urlpatterns = [
    path('admin/', admin.site.urls),

    path('greeting/', greeting),
    path('rate/list/', rate_list),
    path('contactus/list/', contactus),
]
