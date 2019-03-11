from  celery import Celery

#创建一个celery类的实例对象
Celery('celery_tasks.tasks',broker='')