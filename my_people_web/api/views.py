from django.shortcuts import HttpResponse
from rest_framework.views import APIView
from api import models
from api import func
from api.utils.throttle import VisitThrottle
# 一些常量
num = list('123456789')
zm = list('qwertyuioplkjhgfdsazxcvbnm')


class Login(APIView):
    # self.dispatch

    authentication_classes = []

    def post(self, request, *args, **kwargs):

        user = request._request.POST.get('username')
        password = request._request.POST.get('password')

        obj = models.UserInfo.objects.filter(username=user, password=password).first()
        if obj:
            token = func.md5(user)
            models.UserToken.objects.update_or_create(user=obj, defaults={'token': token})
            return HttpResponse('登陆成功！')
        else:
            return HttpResponse('登陆失败')


class Register(APIView):
    throttle_classes = [VisitThrottle, ]
    authentication_classes = []
    def post(self, request, *args, **kwargs):

        user = request._request.POST.get('username')
        password = request._request.POST.get('password')

        if_name = models.UserInfo.objects.filter(username=user).first()

        if if_name:
            return HttpResponse('用户名已存在')
        elif len(password) < 8:
            return HttpResponse('密码长度应不小于8')
        elif password.isdigit() or password.isalpha():
            return HttpResponse('密码至少为数字与字母的结合')
        models.UserInfo.objects.update_or_create(defaults={'username': user,
                                                           'password': password})
        return HttpResponse('用户创建成功，用户名为：%s, 密码为：%s' % (user, password))


class Content(APIView):

    pass



