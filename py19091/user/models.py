# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class User(models.Model):
    tel = models.CharField(unique=True, max_length=11)
    password = models.CharField(max_length=32)
    status = models.IntegerField(blank=True, null=True)
    reg_time = models.DateTimeField(blank=True, null=True, auto_now=True)
    alipay_user_id = models.CharField(max_length=100, blank=True, null=True)
    qq_user_id = models.CharField(max_length=100, blank=True, null=True)
    wx_user_id = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_user'


class UserFriend(models.Model):
    # user_id = models.IntegerField(blank=True, null=True)
    # friend_id = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='users', blank=True)
    friend = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='friends', blank=True)
    create_time = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        managed = False
        db_table = 't_user_friend'


class UserInfo(models.Model):
    email = models.CharField(max_length=50)
    birth = models.DateField(blank=True, null=True)
    nickname = models.CharField(max_length=100, blank=True, null=True)
    realname = models.CharField(max_length=100, blank=True, null=True)
    sex = models.CharField(max_length=1, blank=True, null=True)
    photo = models.BinaryField(blank=True, null=True)
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name='info', blank=True)

    class Meta:
        managed = False
        db_table = 't_user_info'


class Role(models.Model):
    name = models.CharField(max_length=100, verbose_name="角色名")
    users = models.ManyToManyField(to=User, db_table="t_role_user", related_name='role', blank=True, null=True)

    class Meta:
        db_table = "t_role"


class Logger(models.Model):
    realname = models.CharField(max_length=100, blank=True, null=True)
    func_name = models.CharField(max_length=200, blank=True, null=True)
    func_param = models.CharField(max_length=200, blank=True, null=True)
    request_url = models.CharField(max_length=100, blank=True, null=True)
    exception_code = models.CharField(max_length=20, blank=True, null=True)
    exception_msg = models.TextField(blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        managed = False
        db_table = 't_logger'
