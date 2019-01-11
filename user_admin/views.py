import string
import random
import time
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import JsonResponse
from django.urls import reverse
from .forms import LoginForm, RegForm, ChangeNicknameForm, BindEmailForm
from .models import Profile


def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        # is_valid里已经包含了对user的验证；当is_valid通过，说明该user也验证通过
        if login_form.is_valid():
            # 如果表单中数据验证通过
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('url_home')))
    else:
        login_form = LoginForm()    # 如果是GET请求，则返回一个空的表单

    # 如果是POST方法，但数据验证不通过，则返回当前页，且表单中原来的数据也会被保留
    context = dict()
    context['login_form'] = login_form
    return render(request, 'user_admin/login.html', context)


def logout(request):    # 登出
    auth.logout(request)
    return redirect(request.GET.get('from', reverse('url_home')))


def register(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST)
        # is_valid里已经包含了对user的验证；当is_valid通过，说明该user也验证通过
        if reg_form.is_valid():
            # 如果表单中数据验证通过
            username = reg_form.cleaned_data['username']
            password = reg_form.cleaned_data['password_again']
            email = reg_form.cleaned_data['email']
            user = User.objects.create_user(username, email, password)
            user.save()

            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('url_home')))
    else:
        reg_form = RegForm()    # 如果是GET请求，则返回一个空的表单

    # 如果是POST方法，但数据验证不通过，则返回当前页，且表单中原来的数据也会被保留
    context = dict()
    context['reg_form'] = reg_form
    return render(request, 'user_admin/register.html', context)


# 展示个人信息
def user_info(request):
    context = dict()
    return render(request, 'user_admin/user_info.html', context)


# 修改昵称，使用通用的form表单+通用模版
def change_nickname(request):
    redirect_to = request.GET.get('from', reverse('url_home'))
    if request.method == 'POST':
        # 实例化ChangeNicknameForm时，将request中的user信息作为参数传递进去，供校验登录状态用
        form = ChangeNicknameForm(request.POST, user=request.user)
        if form.is_valid():
            nickname_new = form.cleaned_data['nickname_new']
            profile, created = Profile.objects.get_or_create(user = request.user)
            profile.nickname = nickname_new
            profile.save()
            return redirect(redirect_to)
    else:
        form = ChangeNicknameForm()
    context = dict()
    context['page_title'] = '个人信息|修改昵称'
    context['form_title'] = '修改昵称'
    context['submit_text'] = '提交修改'
    context['return_back_url'] = redirect_to
    context['form'] = form
    return render(request, 'form.html', context)


# 绑定邮箱
def bind_email(request):
    redirect_to = request.GET.get('from', reverse('url_home'))
    if request.method == 'POST':
        # 实例化BindEmailForm时，将request作为参数传递进去
        # request包含的user和session['bind_email_code']信息，供后台校验登录态和验证码用
        form = BindEmailForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            request.user.email = email
            request.user.save()
            return redirect(redirect_to)
    else:
        form = BindEmailForm()
    context = dict()
    context['page_title'] = '个人信息|绑定Email'
    context['form_title'] = '绑定Email'
    context['submit_text'] = '提交'
    context['return_back_url'] = redirect_to
    context['form'] = form

    return render(request, 'user_admin/bind_email.html', context)    # form.html做成了一个通用模版 多个功能可共用


# 发送验证码至邮箱
def send_verifi_code(request):
    email_addr = request.GET.get('email_addr', '')
    data = dict()
    if email_addr != '':
        # 生成验证码，随机使用52个ASCII码字母和10个数字，生成一个4位的随机码，返回值是一个list
        list = random.sample(string.ascii_letters + string.digits, 4)
        code = ''.join(list)    # 装list转换成字符串


        send_code_time = request.session.get('send_code_time', 0)
        now = int(time.time())
        if now - send_code_time < 20:       # 后台控制验证码发送频率，不能小于20秒
            data['status'] = 'ERROR - from send-code-time'
        else:
            request.session['bind_email_code'] = code  # 将验证码暂时存入session(默认有效期为2周)
            request.session['send_code_time'] = now # 刷新最近一次发送验证码时间
            # 发送邮件
            send_mail(
                '绑定邮箱',
                '验证码：%s' % code,
                '275799285@qq.com',
                [email_addr],
                fail_silently=False,
            )
            data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)
