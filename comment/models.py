from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

class Comment(models.Model):
    # 评论对象，通过contentType来指定评论对象，可以是某个blog 也可以是其他
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()  # 对应模型的主键值
    content_object = GenericForeignKey('content_type', 'object_id')

    comment_text = models.TextField()   # 评论内容
    comment_time = models.DateTimeField(auto_now_add=True)  # 评论时间，创建时自动添加评论时间
    comment_user = models.ForeignKey(User, on_delete=models.DO_NOTHING) # 评论者，通过外键与django的User表关联

    class Meta:
        ordering = ['-comment_time']    # 设置排序方式，以created_time倒序