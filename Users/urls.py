from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('signin/', views.user_signin, name='user_signin'),
    path('signup/', views.user_signup, name='user_signup'),
    path('signout/', views.user_signout, name='user_signout'),

    # Dashboard
    path('dashboard/', views.user_dashboard, name='user_dashboard'),

    # NEW: Payment API Endpoint (Called by JavaScript)
    path('api/pay/', views.initiate_payment, name='initiate_payment'),

    # Application Detail
    path('application/<int:app_id>/', views.app_detail, name='app_detail'),

    path('', views.user_signin, name='user_home'),
]