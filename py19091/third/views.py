import hashlib

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import urlquote
from . import zfb_conf
from py19091 import db
from alipay.aop.api.domain.AlipayOpenAuthTokenAppModel import AlipayOpenAuthTokenAppModel
from alipay.aop.api.request.AlipayOpenAuthTokenAppRequest import AlipayOpenAuthTokenAppRequest
from alipay.aop.api.response.AlipayOpenAuthTokenAppResponse import AlipayOpenAuthTokenAppResponse


def zfb_login(request):
    login_url = zfb_conf.LOGIN_URL
    app_id = zfb_conf.APPID
    redirect_url = urlquote(zfb_conf.REDIRECT_URL)
    return redirect(to=f"{login_url}?app_id={app_id}&redirect_uri={redirect_url}")


def zfb_callback(request):
    # 获取支付宝授权码
    app_auth_code = request.GET.get("app_auth_code")

    # 直接获取客户端对象
    alipay_client = zfb_conf.get_alipay_client()
    # 创建一个模型对象，用来接收接口参数
    biz_model = AlipayOpenAuthTokenAppModel()
    biz_model.grant_type = "authorization_code"
    biz_model.code = app_auth_code

    # 创建一个接口对应的请求对象
    alipay_request = AlipayOpenAuthTokenAppRequest(biz_model=biz_model)

    # 调用接口
    response_content = alipay_client.execute(alipay_request)

    # 创建一个响应对象，用来处理接口返回的内容
    alipay_response = AlipayOpenAuthTokenAppResponse()

    # 处理结果
    alipay_response.parse_response_content(response_content)
    print(alipay_response)
    # 获取支付宝用户id
    if alipay_response.is_success():
        alipay_user_id = alipay_response.user_id
        # 根据支付宝用户id 查询该用户是否和本网站账号进行了绑定
        sql = "select * from t_user where alipay_user_id = %s"
        user = db.query_one(sql, args=(alipay_user_id,))
        if user is None:
            # 未绑定，绑定账号
            return render(request, 'bind.html', {"alipay_user_id": alipay_user_id})

        # 如果绑定，直接登录
        if user.get("status") == 1:
            return render(request, "next_base.html", {"user_id": user.id})

        if user.get("status") == 3:
            return render(request, "index.html", {"msg": "您的账户已被冻结，请联系管理员"})

        request.session["LOGIN_LOCAL_FLAG"] = user
        return redirect(to="/")
    request.session["msg"] = '支付宝登录失败'
    return redirect(to="/")


def zfb_bind(request):
    '''
    绑定账号
    :param request:
    :return:
    '''
    alipay_user_id = request.POST.get("alipay_user_id")
    qq_user_id = request.POST.get("qq_user_id")
    wx_user_id = request.POST.get("wx_user_id")
    tel = request.POST.get("tel")
    pwd = request.POST.get("password")
    pwd = hashlib.md5(pwd.encode(encoding='utf-8')).hexdigest()
    sql = "select * from t_user where tel=%s"
    user = db.query_one(sql, args=(tel,))
    if user is None:
        return JsonResponse({"bind_msg": "该账户不存在"})
    # 密码错误情况
    if user.get("password") != pwd:
        return JsonResponse({"bind_msg": "密码错误"})
    sql = "update t_user set alipay_user_id=%s where tel=%s"
    if alipay_user_id != '':
        db.update(sql, args=(alipay_user_id, tel))
    if qq_user_id != '':
        db.update(sql, args=(qq_user_id,))
    if wx_user_id != '':
        db.update(sql, args=(wx_user_id,))
    return JsonResponse({"bind_msg": "绑定成功"})


def register(request):
    '''
    没有账号绑定
    :param request:
    :return:
    '''
    params = request.GET.dict()
    # 遍历获取params中值不为空串的键值对
    key_list = list(params.keys())
    for e in key_list:
        if params[e] != '':
            third_user_id = params[e]
            third_type = e
    return render(request, 'register.html', {"third_user_id": third_user_id, "third_type": third_type})