from django.urls import path
from rest_framework.routers import DefaultRouter
from api import views

app_name = 'api'

router = DefaultRouter()
router.register('contactus', views.ContactUsViewSet, basename='contactus')


urlpatterns = [
    path('source/', views.SourceViewSet.as_view(), name='sources'),
    path('rates/', views.RatesView.as_view(), name='rates'),
    path('rates/<int:pk>/', views.RateDetailsView.as_view(), name='rate-details'),
]


urlpatterns += router.urls
