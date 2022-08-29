from django.urls import path
from accounts import views

app_name = 'accounts'


urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('activate/<uuid:username>/', views.UserActivateView.as_view(), name='user_activate'),
    path('signup/done/', views.SignUPDoneView.as_view(), name='signup_done'),

]
