from django.urls import path
from . import views


# APP子路由
# 子路由的好处：(1)给总路由瘦身 (2)降低APP与Project的耦合
urlpatterns = [
    path('update_comment', views.update_comment, name='url_update_comment'),
]