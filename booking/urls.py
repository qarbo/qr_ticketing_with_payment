from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from . import views

urlpatterns = [
    path('create-checkout-session/', views.checkout, name='create_checkout_session'),
    path('success/', views.success, name='success'),
    path('', views.booking_page, name='booking_page'),
    path('last_booking/<str:booking_id>', views.last_booking, name='last_booking'),
    path('<int:pk>/delete/', views.delete_booking, name='delete_booking'),
    path('generate-qr-code/<str:booking_id>/', views.generate_qr_code, name='generate_qr_code'),
    path('get-price/', views.get_price, name='get_price'),
    path('scan/', views.scan_booking, name='scan_booking'),
    # path('reminder/', views.reminder, name='reminder'),
] + staticfiles_urlpatterns()
