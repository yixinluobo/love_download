from django.conf.urls import url
from django.urls import path
from . import views

app_name = "res"
urlpatterns = [
    path("upload", views.upload, name="upload"),
    url(r"detail/(?P<pk>\d+)", views.detail, name="detail"),
    path("download/<int:pk>", views.download, name="download"),
    path("comment/<int:re_id>", views.comment, name="comment"),
]
