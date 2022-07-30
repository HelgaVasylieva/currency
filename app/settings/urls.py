from django.contrib import admin
from django.urls import path

from currency.views import rate_list, contactus, index, rate_create, rate_update, rate_details, rate_delete, \
    source_list, source_create, source_update, source_details, source_delete

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', index),
    path('rate/list/', rate_list),
    path('contactus/list/', contactus),
    path('rate/create/', rate_create),
    path('rate/update/<int:rate_id>/', rate_update),
    path('rate/details/<int:rate_id>/', rate_details),
    path('rate/delete/<int:rate_id>/', rate_delete),
    path('source/list/', source_list),
    path('source/create/', source_create),
    path('source/update/<int:source_id>/', source_update),
    path('source/details/<int:source_id>/', source_details),
    path('source/delete/<int:source_id>/', source_delete),


]
