from django.urls import path
from . import views

app_name = "user"
urlpatterns = [
    path("personal", views.personal, name="personal"),
    path("point", views.point, name="point"),
    path("modifypass", views.modifypass, name="modifypass"),
    path("photo/<int:pk>", views.photo, name="photo"),
    path("collection/<int:re_id>", views.collection, name="collection"),
    path("find_password", views.find_password, name="find_password"),
    path("follow/<int:friend_id>", views.follow, name="follow"),
]