"""py19091 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url('^$', views.index, name='index'),
    # url('^bbs', views.bbs, name='bbs'),
    url('^register', views.register, name="register"),
    url('^next_base', views.next_base, name="next_base"),
    path("success/<int:user_id>", views.success, name='success'),
    path("check/<tel>", views.check_tel, name="check_tel"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("photo", views.photo, name="photo"),
    url('^user/', include('user.urls')),
    url('^res/', include('resource.urls')),
    url('^third/', include('third.urls')),
    url('^bbs/', include('bbs.urls')),
    path("friend", views.friend, name="friend"),
]
