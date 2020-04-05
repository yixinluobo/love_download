from django.contrib import admin

# Register your models here.
from user.models import *


# admin.site.register(User)
@admin.register(User)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ("tel", "status", "reg_time")


@admin.register(UserInfo)
class UserInfoModelAdmin(admin.ModelAdmin):
    list_display = ("id", "nickname")


@admin.register(UserFriend)
class UserFriendModelAdmin(admin.ModelAdmin):
    list_display = ("user_id", "friend_id", "create_time")
