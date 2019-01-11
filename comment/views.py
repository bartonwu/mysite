from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.http import JsonResponse
from .models import Comment
from .forms import CommentForm


# 提交评论
def update_comment(request):
    referer = request.META.get('HTTP_REFERER', reverse('url_home'))
    data = dict()
    # 实例化ComentForm表单时，给它传递一个user对象的参数，供form内部校验用
    comment_form = CommentForm(request.POST, user=request.user)
    if comment_form.is_valid():
        # 检查通过，则写入数据库
        comment = Comment()
        comment.comment_user = comment_form.cleaned_data['user']
        comment.comment_text = comment_form.cleaned_data['text']
        # 只需给content_object赋值即可，object_id, content_type不需要额外赋值
        comment.content_object = comment_form.cleaned_data['content_object']
        comment.save()
        # return redirect(referer)
        # ajax的请求在后台执行成功后，将相关数据返回给前端显示
        data['status'] = 'SUCCESS'
        data['username'] = comment.comment_user.username
        data['comment_time'] = comment.comment_time.strftime('%Y-%m-%d %H:%M:%S')
        data['text'] = comment.comment_text
    else:
        # return render(request, 'error.html', {'message': comment_form.errors, 'redirect_to': referer})
        data['status'] = 'FAIL'
        data['message'] = list(comment_form.errors.values())[0][0]
    return JsonResponse(data)
