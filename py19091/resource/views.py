from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import urlquote

from py19091 import db
from py19091.decorators import auth_session, score_setting
from datetime import datetime
import uuid

from user.models import User
from .forms import ResourceModelForm


# Create your views here.
@auth_session
@score_setting(action="2")
def upload(request):
    '''
    上传
    :param quest:
    :return:
    '''
    if request.method == "GET":
        return render(request, 'upload.html')

    form = ResourceModelForm(request.POST, files=request.FILES)

    # 对表单进行校验
    form.is_valid()

    # 进行数据的保存， 获取资源模型
    resource = form.instance

    # 获取当前登录的用户ID
    user_id = db.get_current_user_id(request)
    # 获取对应的用户模型
    user = User.objects.get(pk=user_id)

    resource.user = user
    # 获取文件
    file = request.FILES.get("re_path")
    # 添加后缀
    houzhui = file.name.split(".")[-1]
    resource.re_suffix = houzhui
    # 添加资源大小
    resource.re_size = file.size
    # 添加资源真实名
    resource.real_name = file.name

    # 保存
    resource.save()

    # # 将文件转成流
    # _file = file.read()
    # 获取其他信息
    # msg = request.POST.dict()
    # # 解决文件重名
    # real_name = uuid.uuid4().hex
    # with open("big_file/{0}.{1}".format(real_name, houzhui), "wb") as fw:
    #     # fw.write(_file)
    #     for _file in file.chunks():
    #         fw.write(_file)
    #     fw.close()
    #
    # msg.setdefault("re_path", "F:\\第三阶段code\\Django项目\\py19091\\big_file\\{0}.{1}".format(real_name, houzhui))
    # msg.setdefault("download_num", 0)
    # msg.setdefault("re_suffix", houzhui)
    # msg.setdefault("upload_time", datetime.now())
    # msg.setdefault("user_id", user_id)
    # msg.setdefault("re_size", file.size)
    # msg.setdefault("real_name", real_name)

    # sql = "insert into resource_info (re_path,re_name,re_type,key_words,re_point," \
    #       "re_desc,download_num,re_suffix,upload_time,user_id,re_size,real_name) values" \
    #       "(%(re_path)s,%(re_name)s,%(re_type)s,%(key_words)s,%(re_point)s,%(re_desc)s," \
    #       "%(download_num)s,%(re_suffix)s,%(upload_time)s,%(user_id)s,%(re_size)s,%(real_name)s)"
    # db.update(sql, args=msg)
    #
    # sql = "insert into t_point (point,ch_time,source,user_id) values (8,now(),2,%s)"
    # db.update(sql, args=(user_id,))

    return render(request, 'upload.html', {"tips": "上传成功"})


def detail(request, pk):
    '''
    资源详情
    :param request:
    :return:
    '''
    # 获取下载信息
    download_msg = request.session.get(db.DOWNLOAD_MSG)
    sql = '''
        select r.id,r.re_suffix,r.re_name,r.upload_time,r.re_size,r.key_words,r.re_desc,
         r.re_point,r.download_num,u.photo,u.nickname, u.user_id
         from resource_info r inner join 
        t_user_info u on r.user_id=u.user_id 
        where r.id=%s
    '''
    msg = db.query_one(sql, args=(pk,))
    msg.setdefault("download_msg", download_msg)

    # 读取资源评论
    sql = """select c.*, u.nickname from t_resource_comment c 
            left join t_user_info u on c.user_id=u.user_id
            where c.re_id=%s
        """
    comment_msg = db.query_list(sql, args=(pk,))
    # 获得总评论数
    sql = 'select count(id) as c_count from t_resource_comment where re_id=%s'
    comment_count = db.query_one(sql, args=(pk,))
    # 计算评星总评分
    # 平均法：
    # sql = "select sum(star) as star_sum from t_resource_comment where re_id=%s"
    # star_sum = db.query_one(sql, args=(pk,))
    # 评星平均分
    # star_avg = int(star_sum.get("star_sum")/comment_count.get("c_count"))
    # 存储过程法：
    re_star = db.query_proc_one("get_res_star3", args=(pk,))
    star_avg = 0 if re_star is None else re_star.get("v_s")
    return render(request, "detail.html",
                  {"msg": msg, "comment_msg": comment_msg, "comment_count": comment_count, "star_avg": star_avg})


@auth_session
@score_setting(action=4)
def download(request, pk):
    '''
    下载资源
    :param request:
    :return:
    '''
    user_id = db.get_current_user_id(request)
    sql = 'select user_id, re_path, re_point, re_name, re_suffix from resource_info where id=%s'
    re = db.query_one(sql, args=(pk,))
    re_path = re.get("re_path")

    # 判断是否为自己上传的资源
    if user_id != re.get("user_id"):
        # 判断当前用户积分是否足够
        sql = "select sum(point) as sum_point from t_point where user_id=%s"
        query_res = db.query_one(sql, args=(user_id,))
        sum_point = query_res.get("sum_point")
        if sum_point < re.get("re_point"):
            request.session.setdefault(db.DOWNLOAD_MSG, "您的积分不足")
            return redirect(to="res:detail", **{"pk": pk})

        # 最后一次下载时间
        sql = '''
            select count(1) as record from t_resource_download where user_id=%s
            and re_id=%s and download_time >= DATE_SUB(now(), INTERVAL 1 MONTH)
        '''
        last_month_down_count = db.query_one(sql, args=(user_id, pk))
        if last_month_down_count.get("record") == 0:
            sql = """
                    insert into t_point (point, ch_time, source, user_id)
                    values (%s, now(), %s, %s)
                """
            # 下载扣分
            point = -(re.get("re_point"))
            db.update(sql, args=(point, 4, user_id))
            # 赠送给上传者积分
            db.update(sql, args=(re.get("re_point"), 6, re.get("user_id")))

        # 向资源下载表中写入记录
        sql = "insert into t_resource_download (user_id, re_id, download_time) values (%s, %s, now())"
        db.update(sql, args=(user_id, pk))

    # 增加下载次数
    sql = "select download_num from resource_info where id=%s"
    old_num = db.query_one(sql, args=(pk,)).get("download_num")
    sql = "update resource_info set download_num=%s where id=%s"
    db.update(sql, args=(old_num + 1, pk))

    # 迭代读取
    def file_iterator(fn, chunk_size=512):
        while True:
            c = fn.read(chunk_size)
            if c:
                yield c
            else:
                break

    fn = open(re_path, "rb")
    response = HttpResponse(file_iterator(fn))
    file_name = "{0}.{1}".format(re.get("re_name"), re.get("re_suffix"))
    file_name = urlquote(file_name)
    response['Content-Type'] = 'application/octet-stream'
    response["Content-Disposition"] = "attachment;filename=" + file_name

    return response


@auth_session
@score_setting(action=3)
def comment(request, re_id):
    '''
    用户评论
    :param request:
    :param user_id:
    :return:
    '''
    # 获得当前登录用户id
    user_id = db.get_current_user_id(request)
    # 获取评论信息
    comment_msg = request.POST.dict()
    comment_msg["user_id"] = user_id
    comment_msg["re_id"] = re_id
    # 将评论信息写入数据库
    sql = """
        insert into t_resource_comment (star, content, comment_time, user_id, re_id)
        values (%(star)s,%(content)s,now(),%(user_id)s,%(re_id)s)
    """
    # 执行SQL并获得主键
    pk = db.update(sql, args=comment_msg)
    # 根据评论的 ID ，查询 评论的人，头像，时间，星级，和内容
    sql = """
        select c.*, u.nickname from t_resource_comment c 
        left join t_user_info u on c.user_id=u.user_id
        where c.id=%s
    """
    comments = db.query_one(sql, args=(pk,))
    # print(comments)
    return JsonResponse(comments)
