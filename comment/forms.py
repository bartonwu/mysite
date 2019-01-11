from django import forms
from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist
from ckeditor.widgets import CKEditorWidget

class CommentForm(forms.Form):
    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    # text字段设置成ckeditor,并且显示样式适用settings中的comment_ckeditor配置项
    text = forms.CharField(widget=CKEditorWidget(config_name='comment_ckeditor'))

    # 接收从views方法中实例化时，传进来的参数user
    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(CommentForm, self).__init__(*args, **kwargs)

    def clean(self):
        # 判断用户是否登录，未登录不允许评论
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用户尚未登录')

        # 评论对象验证
        content_type = self.cleaned_data['content_type']
        object_id = self.cleaned_data['object_id']
        try:
            # 根据前端获取到的字符串,如'blog'，获取对应的model类名，如 class Blog
            model_class = ContentType.objects.get(model=content_type).model_class()
            # 根据model类名和pk值(object_id)获取被评论的目标对象
            model_obj = model_class.objects.get(pk=object_id)
            self.cleaned_data['content_object'] = model_obj
        except ObjectDoesNotExist:
            raise forms.ValidationError('评论对象不存在')
        return self.cleaned_data