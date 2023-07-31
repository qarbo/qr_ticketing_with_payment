from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
] + staticfiles_urlpatterns()
