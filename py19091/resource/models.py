# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from user.models import User


class ResourceInfo(models.Model):
    re_path = models.FileField(upload_to="big_file", max_length=255, blank=True, null=True)
    re_name = models.CharField(max_length=20, blank=True, null=True)
    re_type = models.CharField(max_length=20, blank=True, null=True)
    key_words = models.CharField(max_length=50, blank=True, null=True)
    re_point = models.IntegerField(blank=True, null=True)
    re_desc = models.CharField(max_length=255, blank=True, null=True)
    download_num = models.IntegerField(blank=True, null=True, default=0)
    re_suffix = models.CharField(max_length=20, blank=True, null=True)
    upload_time = models.DateField(blank=True, null=True, auto_now=True)
    # user_id = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='resources', blank=True, null=True)
    re_size = models.FloatField(blank=True, null=True)
    real_name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'resource_info'


class Point(models.Model):
    point = models.IntegerField()
    ch_time = models.DateTimeField(blank=True, null=True, auto_now=True)
    source = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_point'


class ResourceComment(models.Model):
    star = models.IntegerField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    comment_time = models.DateTimeField(blank=True, null=True, auto_now=True)
    user_id = models.IntegerField(blank=True, null=True)
    re_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_resource_comment'


class ResourceDownload(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    re_id = models.IntegerField(blank=True, null=True)
    download_time = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        managed = False
        db_table = 't_resource_download'


class ScoreConf(models.Model):
    action = models.IntegerField(blank=True, null=True)
    score = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_score_conf'


class StarConf(models.Model):
    star = models.IntegerField(blank=True, primary_key=True)
    comment_num = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_star_conf'


class Collection(models.Model):
    re_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    coll_time = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        managed = False
        db_table = 't_collection'
