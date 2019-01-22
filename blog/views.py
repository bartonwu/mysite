from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
from django.contrib.contenttypes.models import ContentType
from .models import Blog, BlogType
from read_statistics import utils
from django.conf import settings
from comment.models import Comment
from comment.forms import CommentForm


# 将blogs数据分好页，并将通用数据写入context字典中
def get_blog_list_common_data(request, blogs_all_list):
    paginator = Paginator(blogs_all_list, settings.BLOGS_NUM_OF_EACH_PAGE)  # 每页num条数据进行分页
    page_num = request.GET.get('page', 1)  # 从GET请求中，获取url中的页码参数(page)，获取不到默认就为1
    page_of_blogs = paginator.get_page(page_num)  # 当page_num为非数字或其他非法字符时，get_page默认返回1，即第1页

    current_page_num = page_of_blogs.number  # 获取当前页码
    # 设置前端页面分页控件，需要显示的页码范围：当前页+当前页前后各两页
    # page_range = [current_page_num-2, current_page_num-1, current_page_num, current_page_num+1, current_page_num+2]
    page_range = list(range(max(current_page_num - 2, 1), current_page_num)) + \
                 list(range(current_page_num, min(current_page_num + 2, paginator.num_pages) + 1))

    # 给不显示的页码加上省略号标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)  # 在page_range list的0号位置，即列表头部，插入元素1
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)  # 在page_range list的尾部，插入总页数,即最大页码

    # 获取blog分类统计数据，按blog_type分类统计
    # 下面这个过程(更容易理解)可以用更简洁的方法来实现： annotate+Count函数
    # blog_types = BlogType.objects.annotate(blog_count=Count('blog'))
    blog_types = BlogType.objects.all()
    blog_types_list = []
    for blog_type in blog_types:
        # 给blogtype对象添加blog_count临时属性，并将blog_type以及对应分类的博客数量存入blog_types_list里
        blog_type.blog_count = Blog.objects.filter(blog_type=blog_type).count()
        blog_types_list.append(blog_type)

    # 获取blog分类统计数据，按createtime中年月分类统计
    blog_dates = Blog.objects.dates('created_time', 'month', order='DESC')
    blog_dates_dict = {}
    # blog_date是日期类型的变量，不是对象，所以不能像blog_type一样直接添加临时属性
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year, created_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count

    context = dict()
    context['page_of_blogs'] = page_of_blogs
    context['blogs'] = page_of_blogs.object_list
    context['blog_types'] = blog_types_list
    context['page_range'] = page_range
    # 获取所有blog中创建日期的所有月份，填充前端按月分类的li
    context['blog_dates'] = blog_dates_dict
    return context


def blog_list(request):
    blogs_all_list = Blog.objects.all()
    context = get_blog_list_common_data(request, blogs_all_list)
    return render(request, 'blog/blog_list.html', context)


def blogs_with_type(request, blog_type_id):
    blog_type = get_object_or_404(BlogType, pk=blog_type_id)
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)
    context = get_blog_list_common_data(request, blogs_all_list)
    context['blog_type'] = blog_type
    return render(request, 'blog/blogs_with_type.html', context)


def blogs_with_date(request, year, month):
    # 按年、月归档：
    blogs_all_list = Blog.objects.filter(created_time__year=year, created_time__month=month)
    context = get_blog_list_common_data(request, blogs_all_list)
    context['date_of_blogs'] = '%s年%s月' % (year, month)
    return render(request, 'blog/blogs_with_date.html', context)


def blog_detail(request, blog_id):  # blog_pk = blog_id,blog主键
    blog = get_object_or_404(Blog, pk=blog_id)
    cookie_key = utils.read_statistics_once_read(request, blog)

    previous_blog = Blog.objects.filter(created_time__gt = blog.created_time).last() # 上一条blog，基于创建时间排序的
    next_blog = Blog.objects.filter(created_time__lt = blog.created_time).first() # 下一条blog，基于创建时间排序的

    # 获取该条blog对应的所有评论
    blog_content_type = ContentType.objects.get_for_model(blog) # 获取blog对应的content_type
    comments = Comment.objects.filter(content_type=blog_content_type, object_id=blog.pk)

    context = dict()
    context['blog'] = blog
    # 当使用render_to_response时，如果需要user信息，需要额外手动添加，因此不推荐使用
    # context['user'] = request.user
    context['previous_blog'] = previous_blog
    context['next_blog'] = next_blog
    context['comments'] = comments

    # 初始化CommentForm表单
    context['comment_form'] = CommentForm(initial={'content_type': blog_content_type.model, 'object_id': blog.pk})

    # response = render_to_response('blog/blog_detail.html', context)
    response = render(request, 'blog/blog_detail.html', context) # 推荐使用render,render方法中带有request参数，已包含user信息
    # setcookie不设置max_age(最长有效期)或expires(过期时间)时，默认关闭浏览器后失效
    response.set_cookie(cookie_key, 'true', max_age=20) # 阅读标记cookie置true
    return response
