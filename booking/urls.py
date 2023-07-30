from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from . import views

urlpatterns = [
    path('create-checkout-session/', views.checkout, name='create_checkout_session'),
    path('success/', views.success, name='success'),
    path('', views.booking_page, name='booking_page'),
    path('last_booking/', views.last_booking, name='last_booking'),
    path('<int:pk>/delete/', views.delete_booking, name='delete_booking'),
    path('generate-qr-code/<str:booking_id>/', views.generate_qr_code, name='generate_qr_code'),
] + staticfiles_urlpatterns()
