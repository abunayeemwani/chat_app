from django.urls import path
from main import views


urlpatterns = [
    path('', views.index),
    path('login', views.login_handle),
    path('logout', views.logout_handle),
]

