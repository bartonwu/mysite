from django.urls import path
from . import views


# APP子路由
# 子路由的好处：(1)给总路由瘦身 (2)降低APP与Project的耦合
urlpatterns = [
    path('login/', views.login, name='url_login'),  # 登录
    path('logout/', views.logout, name='url_logout'),  # 登出
    path('register/', views.register, name='url_register'),  # 注册url
    path('userinfo/', views.user_info, name='url_user_info'),  # 个人信息页
    path('change_nickname/', views.change_nickname, name='url_change_nickname'),  # 修改昵称
    path('bind_email/', views.bind_email, name='url_bind_email'),  # 绑定email
    path('send_verifi_code/', views.send_verifi_code, name='url_send_verifi_code'),  # 发送验证码
]