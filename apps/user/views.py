from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.views.generic import View
from django.http import  HttpResponse
from django.conf import settings
from user.models import User
# from  celery_tasks.tasks import send_register_active_email

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import  SignatureExpired
import re

#user/register
def register(request):

    if request.method == 'GET':
        '''显示注册页面'''
        return render(request,'register.html')
    else:
        # 1、发送过来数据，就要接收数据

        # 3、进行业务处理：进行用户注册
        # 4、返回应答
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')
        # 2、进行数据校验      all可以校验数据
        if not all([username, password, email]):
            return render(request, 'register.html', {'errmsg': '数据不完整'})
        # 校验邮箱
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errmsg': '邮箱不合法'})

        if allow != 'on':
            return render(request, 'register.html', {'errmsg': '请同意协议'})
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            user = None
        if user:
            return render(request, 'register', {'errmsg': '用户名已存在'})

        user = User.objects.create_user(username, email, password)
        user.is_active = 0
        user.save()
        return redirect(reverse('goods:index'))
def register_handle(request):
    #1、发送过来数据，就要接收数据

    #3、进行业务处理：进行用户注册
    #4、返回应答
    username = request.POST.get('user_name')
    password = request.POST.get('pwd')
    email = request.POST.get('email')
    allow = request.POST.get('allow')
    # 2、进行数据校验      all可以校验数据
    if not all([username,password,email]):
        return render(request,'register.html',{'errmsg':'数据不完整'})
    #校验邮箱
    if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$',email):
        return render(request,'register.html',{'errmsg':'邮箱不合法'})

    if allow != 'on':
        return render(request,'register.html',{'errmsg':'请同意协议'})
    try:
        User.objects.get(username=username)
    except User.DoesNotExist:
        user = None
    if user:
        return  render(request,'register' ,{'errmsg':'用户名已存在'})

    user = User.objects.create_user(username,email,password)
    user.is_active = 0
    user.save()

    return redirect(reverse('goods:index'))

#类视图
class RegisterView(View):

    def get(self,request):
        return render(request,'register.html')

    def post(self,request):
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')
        # 2、进行数据校验      all可以校验数据
        if not all([username, password, email]):
            return render(request, 'register.html', {'errmsg': '数据不完整'})
        # 校验邮箱
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errmsg': '邮箱不合法'})

        if allow != 'on':
            return render(request, 'register.html', {'errmsg': '请同意协议'})
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            user = None
        if user:
            return render(request, 'register', {'errmsg': '用户名已存在'})

        user = User.objects.create_user(username, email, password)
        user.is_active = 0
        user.save()
        #发送激活邮件，包含激活链接：http://127.0.0.1:8000/user/active/id
        #对id进行加密 密钥 加密 解密  itsdangerous
        #激活链接中需要包含用户的身份信息

        #加密用户的身份信息，生成激活token
        serializer = Serializer(settings.SECRET_KEY,3600)
        info = {'confirm':user.id}
        token = serializer.dumps(info)
        token = token.decode()

        #发邮件
#        send_register_active_email.delay(email,username,token)
        return redirect(reverse('goods:index'))

class ActiveView(View):
    def get(self,request,token):
        '''用户激活'''
        #进行解密，获取需要激活的用户信息
        serializer = Serializer(settings.SECRE_KEY, 3600)
        try:
            info = serializer.loads(token)
            user_id = info['confirm']

            user = User.objects.get(id = user_id)
            user.is_active = 1
            user.save()

            return redirect(reverse('goods:index'))
        except SignatureExpired as e:
            #激活链接已过期
            return  HttpResponse('激活链接已过期')
            #应该还提示他重新注册 重新发送邮件验证


class LoginView(View):
    def get(self,request):
        return render(request,'login.html')