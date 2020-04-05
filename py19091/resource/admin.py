from django.contrib import admin

# Register your models here.
from .models import *


@admin.register(ResourceInfo)
class ResInfoAdminModel(admin.ModelAdmin):
    list_display = (
        "re_name", "re_type", "key_words", "re_point", "re_desc", "download_num", "re_suffix", "upload_time", "user_id",
        "re_size", "real_name")


@admin.register(Point)
class PointAdminModel(admin.ModelAdmin):
    list_display = ("point", "ch_time", "source", "user_id")


@admin.register(ResourceComment)
class CommentAdminModel(admin.ModelAdmin):
    list_display = ("star", "content", "comment_time", "user_id", "re_id")


@admin.register(ResourceDownload)
class DownloadAdminModel(admin.ModelAdmin):
    list_display = ("user_id", "re_id", "download_time")


@admin.register(ScoreConf)
class ScoreConfAdminModel(admin.ModelAdmin):
    list_display = ("action", "score")


@admin.register(StarConf)
class StartConfAdminModel(admin.ModelAdmin):
    list_display = ("star", "comment_num")


@admin.register(Collection)
class CollectionAdminModel(admin.ModelAdmin):
    list_display = ("re_id", "user_id", "coll_time")
