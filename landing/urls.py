from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('register/', views.register_page, name='register_page'),
    path('booking/', views.booking_page, name='booking_page'),
    path('success/', views.booking_page, name='success_page'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),
    path('stripe-webhook/', views.stripe_webhook, name='stripe_webhook'),

] + staticfiles_urlpatterns()
