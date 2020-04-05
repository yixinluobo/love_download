import copy
import json
from django.utils.deprecation import MiddlewareMixin
from py19091 import db
from user.models import UserInfo, Logger


class LogMiddleware(MiddlewareMixin):

    def process_view(self, request, func, args, kwargs):
        '''

        :param request:
        :param func: 函数
        :param args: 函数参数
        :param kwargs: 函数参数
        :return:
        '''
        user_id = db.get_current_user_id(request)
        if user_id is None:
            return None
        # 获取用户真实姓名
        self.realname = UserInfo.objects.get(user_id=user_id).realname
        self.func_name = ".".join((func.__module__, func.__name__))
        self.func_param = json.dumps(kwargs)
        self.request_url = request.path

    def process_exception(self, request, exception):
        '''
        收集异常信息
        :param request:
        :param exception:
        :return:
        '''
        self.exception_code = exception.args[0]
        self.exception_msg = exception.args[1]

    def process_response(self, request, response):
        '''
        写入日志
        :param request:
        :param response:
        :return:
        '''
        if hasattr(self, "realname"):
            param = self.__dict__
            p = copy.deepcopy(param)
            p.pop("get_response")
            Logger.objects.create(**p)
        return response
