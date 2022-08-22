from django.urls import path
from currency import views

app_name = 'currency'

urlpatterns = [

    path('rate/list/', views.RateListView.as_view(), name='rate_list'),
    path('rate/create/', views.RateCreateView.as_view(), name='rate_create'),
    path('rate/update/<int:pk>/', views.RateUpdateView.as_view(), name='rate_update'),
    path('rate/delete/<int:pk>/', views.RateDeleteView.as_view(), name='rate_delete'),
    path('rate/details/<int:pk>/', views.RateDetailsView.as_view(), name='rate_details'),
    path('rate/download/', views.DownloadRateView.as_view(), name='rate_download'),

    path('contactus/list/', views.ContactListView.as_view(), name='contact_list'),
    path('contactus/create/', views.ContactUsCreateView.as_view(), name='contactus_create'),

    path('source/list/', views.SourceListView.as_view(), name='source_list'),
    path('source/create/', views.SourceCreateView.as_view(), name='source_create'),
    path('source/update/<int:pk>/', views.SourceUpdateView.as_view(), name='source_update'),
    path('source/details/<int:pk>/', views.SourceDetailsView.as_view(), name='source_details'),
    path('source/delete/<int:pk>/', views.SourceDeleteView.as_view(), name='source_delete'),

    path('my-profile/', views.UserProfileView.as_view(), name='my_profile'),

]
