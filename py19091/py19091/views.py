from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from datetime import datetime
import hashlib
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect, csrf_exempt

from user.forms import UserModelForm, UserInfoModelForm
from user.models import User
from . import db
from .decorators import score_setting, auth_session
from django.utils.http import urlquote


def index(request):
    '''
    首页
    :param request:
    :return:
    '''
    try:
        msg = request.session.pop("msg")
    except:
        msg = None

    # 首页第一页展示资料列表
    sql = """select r.id, r.re_suffix,r.re_name,u.nickname,r.upload_time,r.re_point
    from resource_info r inner join 
    t_user_info u on r.user_id=u.user_id 
    order by r.upload_time desc
    """
    re_list = db.query_list(sql)
    # 资源分页
    paginator = Paginator(re_list, 5)
    page_num = request.GET.get("page", 1)
    page = paginator.get_page(page_num)

    return render(request, "index.html", {"msg": msg, "re_list": page})


# def bbs(request):
#     '''
#     论坛
#     :param request:
#     :return:
#     '''
#     return render(request, "bbs.html")


def register(request):
    '''
    注册
    :param request:
    :return:
    '''
    return render(request, 'register.html')


def next_base(request):
    '''
    注册信息
    :param request:
    :return:
    '''
    if request.method == "GET":
        return render(request, "next_base.html")
    # # 获取注册手机号及密码
    # regist_info = request.POST.dict()
    # # print(regist_info)
    # # 判断该手机号码是否已经注册
    # sql = "select * from t_user where tel = %s"
    # user = db.query_one(sql, args=(regist_info.get("tel"),))
    # if user is not None:
    #     return render(request, 'register.html', {"msg": "手机号已被注册", "tel": regist_info.get("tel")})
    #
    # third_type = regist_info.get("third_type")
    # if third_type != '':
    #     sql = "insert into t_user(tel, password, status, reg_time, "+third_type+") values(%(tel)s, MD5(%(password)s), 1, now(),%(third_user_id)s)"
    # else:
    #     sql = "insert into t_user(tel, password, status, reg_time) values(%(tel)s, MD5(%(password)s), 1, now())"
    # pk = db.update(sql, args=regist_info)
    # # print(pk)

    form = UserModelForm(request.POST)
    # 对页面参数进行校验
    if form.is_valid():
        user = form.instance
        # 获取页面密码
        password = user.password
        # 对密码进行MD5加密
        password = hashlib.md5(password.encode(encoding="utf-8")).hexdigest()
        user.password = password
        user.status = 1
        # 将数据保存到表中
        form.save()
        # 获取模型对象主键
        pk = user.pk

        # 获取第三方登录的type和ID
        param = request.POST.dict()
        type = param.get("third_type")
        third_user_id = param.get("third_user_id")
        if type and third_user_id:
            # 更新字段
            column = "alipay_user_id" if type == "1" else "qq_user_id" if type == "2" else "wx_user_id"
            sql = f"update t_user set {column} = %s where id=%s"
            db.update(sql, args=(third_user_id, pk))
        return render(request, 'next_base.html', {"user_id": pk})


@score_setting(action=1)
def success(request, user_id):
    '''
    注册完成
    :param request:
    :return:
    '''
    if request.method == "GET":
        return render(request, "success.html")

    form = UserInfoModelForm(request.POST, files=request.FILES)
    form.is_valid()
    user_info = form.instance
    user_info.user = User.objects.get(pk=user_id)
    # 获取头像
    photo = request.FILES.get("photo")
    _photo = photo.read()
    user_info.photo = _photo
    user_info.save()
    nickname = user_info.nickname

    # 修改账号状态
    user = User.objects.get(pk=user_id)
    user.status = 2
    user.save()

    # # 获取头像
    #     # # print(request.FILES.get("photo"))
    #     # photo = request.FILES.get("photo")
    #     # # 将头像转成流
    #     # _photo = photo.read()
    #     # # 获取其他信息
    #     # msg = request.POST.dict()
    #     # msg.setdefault("photo", _photo)
    #     # msg.setdefault("user_id", user_id)
    #     # # 写入数据库
    #     # sql = "insert into t_user_info (email,birth,nickname,realname,sex,photo,user_id) values" \
    #     #       "(%(email)s,%(birth)s,%(nickname)s,%(realname)s,%(sex)s,%(photo)s,%(user_id)s)"
    #     # new_pk = db.update(sql, args=msg)
    #     # # 信息上传成功，更改用户状态
    #     # sql = "update t_user set status=2 where id=%(user_id)s"
    #     # db.update(sql, args={"user_id": user_id})
    #     # # 用户激活赠送20积分
    #     # # sql = "insert into t_point (point,ch_time,source,user_id) values" \
    #     # #       "(20,now(),1,%(user_id)s)"
    #     # # db.update(sql, args={"user_id": user_id})
    return render(request, "success.html", {"nick_name": nickname, "user_id": user_id})


def check_tel(request, tel):
    sql = "select * from t_user where tel=%s"
    user = db.query_one(sql, args=(tel,))
    if user is None:
        return JsonResponse({"status": True, "msg": ""})

    return JsonResponse({"status": False, "msg": "手机号已被注册"})


# @csrf_protect
@csrf_exempt
def login(request):
    '''
    登录
    :param request:
    :return:
    '''
    login_info = request.POST.dict()
    tel = login_info.get("tel")
    pwd = login_info.get("password")
    pwd = hashlib.md5(pwd.encode(encoding='utf-8')).hexdigest()
    sql = "select * from t_user where tel=%s"
    user = db.query_one(sql, args=(tel,))
    if (user is None) or (pwd != user.get("password")):
        return render(request, "index.html", {"msg": "用户名或密码错误", "tel": tel})

    if user.get("status") == 1:
        return render(request, "next_base.html", {"user_id": user.get("id")})

    if user.get("status") == 3:
        return render(request, "index.html", {"msg": "您的账户已被冻结，请联系管理员", "tel": tel})

    # 处理用户时间不能转换问题
    # user.pop("reg_time")
    # 把用户信息存储到session中
    request.session["LOGIN_LOCAL_FLAG"] = user

    # 获取要跳转的页面
    url = request.POST.get("url")
    if not url:
        return redirect(to=reverse("index"))
    return redirect(to=url)


def logout(request):
    '''
    退出登录
    :param request:
    :return:
    '''
    request.session.clear_expired()

    request.session.flush()
    return redirect(to="/")


@auth_session
def photo(request):
    '''
    显示头像
    :param request:
    :return:
    '''
    user_id = db.get_current_user_id(request)
    # 根据用户id获取用户头像
    sql = "select photo from t_user_info where user_id=%s"
    user = db.query_one(sql, args=(user_id,))
    photo = user.get("photo")

    # 下载文件
    # 解决文件下载中文乱码
    # response = HttpResponse(photo, content_type="image/png")
    # filename = "头像.doc"
    # filename = urlquote(filename)
    # response["Content-Disposition"] = "attachment;filename="+filename
    # response["Content-Disposition"] = "inline;filename=头像.png"

    return HttpResponse(photo, content_type="image/png")


# @auth_session
def friend(request):
    '''
    请求用户信息
    :param request:
    :return:
    '''
    user_id = db.get_current_user_id(request)
    sql = '''
    select f.friend_id user_id, t.realname  from t_user_friend f 
    left join t_user_info t on t.user_id = f.friend_id where f.user_id = %s
    union 
    select f.user_id , t.realname from t_user_friend f left join 
    t_user_info t on f.user_id = t.user_id where f.friend_id = %s
    '''
    friends = db.query_list(sql, args=(user_id, user_id))
    return JsonResponse(friends, safe=False)
