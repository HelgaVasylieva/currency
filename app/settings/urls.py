from django.contrib import admin
from django.urls import path

from currency.views import rate_list, contactus, index

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', index),
    path('rate/list/', rate_list),
    path('contactus/list/', contactus),

]
