from django.db import models
from django.contrib.auth.models import User


# 自定义的用户模型，通过OneToOne外键关联到User模型，并启用级联删除
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='昵称')
    nickname = models.CharField(max_length=20) # 新增自定义字段，昵称

    def __str__(self):
        return '<Profile: %s for %s>' % (self.nickname, self.user.username)


def get_nickname(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return  profile.nickname
    else:
        return ''

# 动态绑定，给User类动态绑定上面的get_nickname方法作为属性
User.get_nickname = get_nickname