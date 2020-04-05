import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'py19091.settings')

# 创建一个Celery对象
# broker : 设置任务存储位置
# backend: 设置任务调用结果存储的位置
app = Celery("py19091", broker="redis://127.0.0.1:6379/6", backend="redis://127.0.0.1:6379/7")

# autodiscover_tasks 会自动去setting.py 去找INSTALLES_APPS对应的应用下的tasks.py(定义任务)文件
app.autodiscover_tasks()
