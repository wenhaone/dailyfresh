# from celery import Celery, app
# from django.core.mail import send_mail
# from django.conf import settings
#
#
# import os
# import django
#
# django.setup() #django的初始化
#
# #创建一个celery类的实例对象
# Celery('celery_tasks.tasks',broker='redis://127.0.0.1:6379/8')#broker中间人（任务队列）
#
# #定义任务函数
# @app.task
# def send_register_active_email(to_email,username,token):
#     '''发送激活邮件'''
#     # 发邮件
#     subject = '优必朋欢迎信息'
#     message = ''
#     sender = settings.EMAIL_FROM
#     receiver = [to_email]
#     html_message = '<h1>欢迎您成为天天生鲜注册会员</h1> %s ,请点击下面链接激活您的账户<br/><a href="http://127.0.0.1:8000/user/active/%s">http://127.0.0.1:8000/user/active/%s</a>' % (
#     username, token, token)
#     send_mail(subject, message, sender, receiver, html_message=html_message)