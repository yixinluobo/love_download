from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views import View

from . import db


def score_setting(action):
    '''
    赠送积分装饰器
    :param action:
    :return:
    '''

    def setting_score(func):
        def setting_score_wrapper(request, *args, **kwargs):
            # 调用视图函数
            response = func(request, *args, **kwargs)
            # 从积分配置表中查询当前对应动作的积分
            sql = "select * from t_score_conf where action=%s"
            conf = db.query_one(sql, args=(action,))
            if conf is None:
                return response
            # 赠送积分
            user_id = None
            if kwargs.get("user_id") is not None and action == 1:
                user_id = kwargs.get("user_id")
            else:
                user_id = db.get_current_user_id(request)
            sql = "insert into t_point (point,ch_time,source,user_id) values" \
                  "(%s,now(),%s,%s)"
            db.update(sql, args=(conf.get("score"), action, user_id))
            return response

        return setting_score_wrapper

    return setting_score


def auth_session(func):
    def auth_session_wrapper(request, *args, **kwargs):
        if isinstance(request, View):
            request = args[0]
        # 验证用户是否登录
        if not request.session.has_key(db.LOGIN_FLAG):
            request.session["msg"] = "未登录，请登录"

            # 获取当前动作的来源地址
            referer = request.headers.get("referer", None)
            if referer is None:
                return redirect(to="/")
            # 判断请求属于同步请求还是异步请求
            if "X-Requested_With" in request.headers:
                return JsonResponse({"url": referer}, status=318)

            return redirect(to="/?url=" + referer)

        # 设置存活时间为30分钟
        lifetime = settings.SESSION_COOKIE_AGE
        request.session.set_expiry(lifetime)
        request.session.clear_expired()
        # 如果用户登陆了，允许访问受保护的资源
        return func(request, *args, **kwargs)

    return auth_session_wrapper
