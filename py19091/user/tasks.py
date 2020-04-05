from celery.task import task
from django.core.mail import EmailMessage
from datetime import datetime


@task()
def celery_async_send_mail(nickname, email, new_pwd):
    time = datetime.now()
    time.strftime("%Y-%m-%d %H:%M:%S")
    body = f'''
                <p>尊敬的用户：{nickname},您于{time}在本网站进行找回密码操作，您的新密码：
                <span style="color:red">{new_pwd}</span> 如不是本人操作，请尽快修改密码。</p>
            '''
    # 发送邮件
    message = EmailMessage(subject="爱下载-找回密码", body=body, to=[email])
    # 设置邮件以html形式发送
    message.content_subtype = "html"
    # 发送邮件
    message.send()
