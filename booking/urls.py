from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from . import views

urlpatterns = [
    path('create-checkout-session/', views.checkout, name='create_checkout_session'),
    path('success/', views.success, name='success'),
    path('', views.booking_page, name='booking_page'),
] + staticfiles_urlpatterns()
