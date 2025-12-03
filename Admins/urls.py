from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('signin/', views.admin_signin, name='admin_signin'),
    path('signup/', views.admin_signup, name='admin_signup'),
    path('signout/', views.admin_signout, name='admin_signout'),  # <-- NEW

    # Dashboard
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # Landing Page
    path('', views.admin_signin, name='admin_home'),
]