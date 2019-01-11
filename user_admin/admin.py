from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


# 自定义一个新的UserAdmin，后台管理界面
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'get_nickname', 'email', 'is_staff', 'is_active', 'is_superuser', 'last_login')
    # 显示的列可以是模型字段，也可以是模型方法，但方法必须有返回值
    def get_nickname(self, obj):
        # obj是一个User对象; 因为User和Profile是 OneToOne的关系，
        # 所以User的对象获得一个profile属性，通过该属性获取对应的Profile对象
        return obj.profile.nickname
    # 设置该模型方法在admin后台列中显示的标题
    get_nickname.short_description = '昵称'

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'nickname')