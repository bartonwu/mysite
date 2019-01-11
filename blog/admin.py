from django.contrib import admin
from .models import BlogType, Blog


@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name')


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    # Blog类通过继承ReadNumExpendMethod类，获得了ReadNumExpendMethod下的 get_read_num方法
    # 显示的列，除了可以是模型字段，也可以是模型方法，且方法必须有返回值，比如：get_read_num
    list_display = ('id', 'title', 'blog_type','author', 'get_read_num','created_time', 'last_updated_time')

