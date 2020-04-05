import hashlib

from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from py19091.decorators import auth_session
from py19091 import db
from user.models import User
from user.tasks import celery_async_send_mail
from django.views.decorators.cache import cache_page


# Create your views here.
@auth_session
@cache_page(timeout=60 * 3)
def personal(request):
    '''
    个人信息界面
    :param request:
    :return:
    '''
    # 获取当前用户的id
    user_id = db.get_current_user_id(request)
    # personal = User.objects.get(pk=user_id)
    # user_info = model_to_dict(personal.info)
    sql = """
        select u.*,
        (select sum(p.point) from t_point p where user_id=%s) as point
        from t_user_info u where u.user_id=%s
    """
    user_info = db.query_one(sql, args=(user_id, user_id))

    return render(request, "personal.html", user_info)


@auth_session
def point(request):
    '''
    积分
    :param request:
    :return:
    '''
    user_id = db.get_current_user_id(request)
    # 读取数据库获取页面需要数据
    sql = "select * from t_point where user_id=%(user_id)s"
    point_info = db.query_list(sql, args={"user_id": user_id})
    # print(point_info)
    # 积分分页
    paginator = Paginator(point_info, 5)
    page_num = request.GET.get("page", 1)
    page = paginator.get_page(page_num)

    sql = "select sum(point) as sum_point from t_point where user_id=%s"
    sum_point = db.query_one(sql, args=(user_id,)).get("sum_point")
    # print(point_info)

    return render(request, "point.html", {"user_id": user_id, "point_info": page, "sum_point": sum_point})


@auth_session
def modifypass(request):
    '''
    修改密码
    :param request:
    :return:
    '''
    if request.method == "GET":
        return render(request, "modifypass.html")
    # 获取表单提交数据
    old_pwd = request.POST.get("oldpwd")
    new_pwd = request.POST.get("newpwd")
    old_pwd = hashlib.md5(old_pwd.encode(encoding='utf-8')).hexdigest()

    user_id = db.get_current_user_id(request)
    sql = "select password from t_user where id=%s"
    sql_pwd = db.query_one(sql, args=(user_id,))
    if old_pwd == sql_pwd.get("password"):
        sql = "update t_user set password=MD5(%s) where id=%s"
        db.update(sql, args=(new_pwd, user_id))
        return redirect(to="/user/personal")
    return render(request, "modifypass.html", {"msg": "旧密码不正确"})


def photo(request, pk):
    '''
    显示不同用户头像
    :param request:
    :return:
    '''
    sql = "select photo from t_user_info where user_id=%s"
    user = db.query_one(sql, args=(pk,))
    photo = user.get("photo")
    return HttpResponse(photo, content_type="image/png")


@auth_session
def collection(request, re_id):
    '''
    收藏资源
    :param request:
    :return:
    '''
    user_id = db.get_current_user_id(request)
    if request.method == "GET":
        sql = """
            select c.coll_time,r.id,r.re_name,r.re_point,r.re_suffix,u.nickname
            from t_collection c left join resource_info r on c.re_id=r.id 
            left join t_user_info u on r.user_id=u.user_id 
            where c.user_id=%s
        """
        coll_list = db.query_list(sql, args=(user_id,))
        # 分页
        paginator = Paginator(coll_list, 10)
        page_num = request.GET.get("page", 1)
        page = paginator.get_page(page_num)
        return render(request, 'collection.html', {"coll_list": page})

    sql = "select * from t_collection where re_id=%s and user_id=%s"
    coll_msg = db.query_one(sql, args=(re_id, user_id))
    if coll_msg:
        return JsonResponse({"data": "已收藏"})
    sql = "insert into t_collection (re_id,user_id,coll_time) values (%s,%s,now())"
    db.update(sql, args=(re_id, user_id))
    return JsonResponse({"data": "收藏成功"})


@auth_session
def follow(request, friend_id):
    '''
    关注
    :param request:
    :return:
    '''
    user_id = db.get_current_user_id(request)
    if request.method == 'GET':
        return render(request, "follow.html")

    sql = "select friend_id from t_user_friend where user_id=%s"
    friend = db.query_one(sql, args=(user_id,))
    if friend:
        return JsonResponse({"msg": "已关注！无需重复关注"})
    sql = "insert into t_user_friend (user_id, friend_id, create_time) values (%s,%s,now())"
    db.update(sql, args=(user_id, friend_id))
    return JsonResponse({"msg": "关注成功"})


def find_password(request):
    '''
    找回密码
    :param request:
    :return:
    '''
    if request.method == "GET":
        return render(request, "find_password.html")

    # 接受页面参数
    post_msg = request.POST.dict()
    find_type = post_msg.get("type")
    tel = post_msg.get("tel")
    email = post_msg.get("certificate")

    if find_type == "email":
        # 判断账户是否存在
        sql = "select u.*,f.email,f.nickname from t_user u left join t_user_info f on u.id=f.user_id where u.tel=%s"
        user = db.query_one(sql, args=(tel,))
        if user is None:
            return JsonResponse({"msg": "账号不存在", "status": False})
            # return render(request, "find_password.html", {"tel": "账号不存在"})
        # 判断邮箱是否存在
        if user.get("email") != email:
            return JsonResponse({"msg": "邮箱必须是注册绑定邮箱", "status": False})
            # return render(request, "find_password.html", {"email": "邮箱必须是注册绑定邮箱"})

        import string, random
        string_random = string.ascii_letters + string.digits
        new_pwd = random.choices(string_random, k=6)
        new_pwd = "".join(new_pwd)

        # 通过异步进行邮件发送
        celery_async_send_mail.delay(user.get("nickname"), email, new_pwd)

        # 修改密码
        sql = "update t_user set password=md5(%s) where tel=%s"
        db.update(sql, args=(new_pwd, tel))

        # 跳转到本页面，并提示邮件已发送
        # request.session["msg"] = "邮件已发送，请用新密码登录"
        return JsonResponse({"msg": "邮件已发送，请用新密码登录"})
