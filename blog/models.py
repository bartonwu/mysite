from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
# from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField
from read_statistics.models import ReadNumExpendMethod, ReadDetail


class BlogType(models.Model):
    type_name = models.CharField(max_length=15)
    def __str__(self):
        return self.type_name


# Blog类通过继承ReadNumExpendMethod类，获得了ReadNumExpendMethod下的 get_read_num方法
class Blog(models.Model, ReadNumExpendMethod):
    title = models.CharField(max_length=50)
    blog_type = models.ForeignKey(BlogType, on_delete=models.DO_NOTHING)
    content = RichTextField()
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    read_details = GenericRelation(ReadDetail)  # 反向关联到ReadDetail模型，blog实例可以直接反问readdetail中对应的数据
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "<Blog: %s>" % self.title

    class Meta:
        ordering = ['-created_time']    # 设置排序方式，以created_time倒序

