from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from currency import views


urlpatterns = [

    path('admin/', admin.site.urls),

    path('', views.IndexView.as_view(), name='index'),

    path('currency/', include('currency.urls')),

    path('auth/', include('django.contrib.auth.urls')),

    path('__debug__/', include('debug_toolbar.urls')),

    path('silk/', include('silk.urls', namespace='silk')),



]
