from django.urls import path
from . import views


urlpatterns = [
    path('home/', views.home, name='home'),

    path('activate_2fa/', views.activate_2fa, name='activate_2fa'),
    path('deactivate_2fa/', views.deactivate_2fa, name='deactivate_2fa'),
    path('verify_2fa/', views.verify_2fa, name='verify_2fa'),
    path('login/', views.login, name='login'),
    
    ]
