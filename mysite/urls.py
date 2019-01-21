"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# from django.conf.urls import handler404, handler500
# from django.conf import settings
# from django.conf.urls.static import static
from . import views

# Project总路由
urlpatterns = [
    path('', views.home, name='url_home'),     # project首页url: localhost:8080/
    path('admin/', admin.site.urls),
    path('blog/', include('blog.blog_urls')),   # blog app分支url: localhost:8080/blog
    path('comment/', include('comment.comment_urls')),  # comment app分支url: localhost:8080/comment
    path('user/', include('user_admin.user_urls')),   # user_admin app分支url: localhost:8080/user
    # 设置ckeditor url
    # path('ckeditor/', include('ckeditor-uploader.urls')),
]

# 自定义404、500页面
handler404 = 'mysite.views.page_not_found'
# handler500 = 'mysite.views.page_error'

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
