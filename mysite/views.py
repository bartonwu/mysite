import datetime
from django.utils import timezone
from django.db.models import Sum
from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from read_statistics import utils
from blog.models import Blog


# 统计最近7日热门点击blog——阅读量前7的blog：
def get_7days_hot_blogs():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    blogs = Blog.objects \
                .filter(read_details__date__lte=today, read_details__date__gt=date) \
                .values('id', 'title') \
                .annotate(read_num_sum=Sum('read_details__read_num')) \
                .order_by('-read_num_sum')  # 利用反向关系，查询blog对应的readdetail对象数据
    return blogs[:7]


# 统计最近30日热门点击blog——阅读量前30的blog：
def get_30days_hot_blogs():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=30)
    blogs = Blog.objects \
                .filter(read_details__date__lte=today, read_details__date__gt=date) \
                .values('id', 'title') \
                .annotate(read_num_sum=Sum('read_details__read_num')) \
                .order_by('-read_num_sum')  # 利用反向关系，查询blog对应的readdetail对象数据
    return blogs[:7]


def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)

    # 统计Blog最近7日的总阅读量趋势数据，供前端图表展示
    dates, blog_read_nums_of_7days = utils.get_read_statistics_7days(blog_content_type)

    # 统计今日hot blog排行
    hot_datas_today = utils.get_today_hot_datas(blog_content_type)

    # 统计昨日hot blog排行
    hot_datas_yesterday = utils.get_yesterday_hot_datas(blog_content_type)

    # 统计最近7日hot blog排行 —— 利用缓存数据
    hot_blogs_7days = cache.get('hot_blogs_7days')
    if hot_blogs_7days is None:
        hot_blogs_7days = get_7days_hot_blogs()
        cache.set('hot_blogs_7days', hot_blogs_7days, 3600)  # 设置缓存，有效时长3600秒
        print('calc - 7days')
    else:
        print('use cache - 7days')

    # 统计最近30日hot blog排行
    hot_blogs_30days = cache.get('hot_blogs_30days')
    if hot_blogs_30days is None:
        hot_blogs_30days = get_30days_hot_blogs()
        cache.set('hot_blogs_30days', hot_blogs_30days, 5)  # 设置缓存，有效时长5秒
        print('calc - 30days')
    else:
        print('use cache - 30days')

    context = dict()
    context['blog_read_nums_of_7days'] = blog_read_nums_of_7days
    context['dates'] = dates
    context['hot_datas_today'] = hot_datas_today
    context['hot_datas_yesterday'] = hot_datas_yesterday
    context['hot_blogs_7days'] = hot_blogs_7days
    context['hot_blogs_30days'] = hot_blogs_30days
    return render(request, 'home.html', context)


