from django.contrib import admin
from django.urls import path

from currency.views import greeting

urlpatterns = [
    path('admin/', admin.site.urls),

    path('greeting/', greeting),
]
