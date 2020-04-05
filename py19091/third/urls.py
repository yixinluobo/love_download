from django.urls import path
from . import views

urlpatterns = [
    path('zfb', views.zfb_login, name="zfb-login"),
    path('zfb_callback', views.zfb_callback, name="zfb_callback"),
    path('zfb_bind', views.zfb_bind, name="zfb_bind"),
    path('register', views.register, name="register"),
]