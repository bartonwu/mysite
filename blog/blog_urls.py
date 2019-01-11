from django.urls import path
from . import views


# APP子路由
# 子路由的好处：(1)给总路由瘦身 (2)降低APP与Project的耦合
urlpatterns = [
    path('', views.blog_list, name='url_blog_list'),  # http://localhost:8000/blog/
    path('<int:blog_id>', views.blog_detail, name="url_blog_detail"),   # http://localhost:8000/blog/int型参数
    path('type/<int:blog_type_id>', views.blogs_with_type, name="url_blogs_with_type"),
    path('date/<int:year>/<int:month>', views.blogs_with_date, name ="url_blogs_with_date"),
]