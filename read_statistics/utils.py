import datetime
from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum
from .models import ReadNum, ReadDetail
from django.utils import timezone


# 某个model(如Blog)下，某个obj(一篇blog实例)的一次阅读计数+1
def read_statistics_once_read(request, obj):
    ct = ContentType.objects.get_for_model(obj)
    key = "%s_%s_read" % (ct.model, obj.pk) # cd.model返回的是对应Model的名称，是一个字符串,如'blog'

    # 通过cookie来判断，只有是新开页面时，才认为是一个有效阅读，计数+1
    if not request.COOKIES.get(key):
        # 总计数+1
        # 存在则取出对应记录，阅读次数+1；不存在则创建，readnum也+1(默认0)
        readnum, created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
        readnum.read_num += 1
        readnum.save()
        # 每日计数+1
        # 存在则取出对应记录，阅读次数+1；不存在则创建，readnum也+1(默认0)
        date = timezone.now().date()
        readDetail, created = ReadDetail.objects.get_or_create(content_type=ct, object_id=obj.pk, date=date)
        readDetail.read_num += 1
        readDetail.save()
    return key  # cookie key返回给views使用


# 统计某个model(如Blog)最近7日的总阅读量趋势,供前端图表使用：
def get_read_statistics_7days(content_type):
    today = timezone.now().date()
    dates = [] # 结果存入列表，因为前端图表显示所需的数据为列表类型
    read_nums_of_7days = [] # 结果存入列表，因为前端图表显示所需的数据为列表类型
    for i in range(6, -1, -1):
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime('%m/%d')) # 将datetime类型的date转成x月x日的字符串格式，供前端图表显示
        # 获取某个model下所有object当天的阅读量，返回一个对象列表
        readDetail_list = ReadDetail.objects.filter(content_type=content_type, date=date)
        # 对list中的所有readDetail对象中的'read_num'字段求和，返回结果为一个字典，字典key为'sum_of_read_num'
        result = readDetail_list.aggregate(sum_of_read_num=Sum('read_num'))
        # 当前面的result['sum_of_read_num']为none时 返回0
        read_nums_of_7days.append(result['sum_of_read_num'] or 0)
    return dates, read_nums_of_7days


# 统计今日热门点击blog——阅读量前7的blog：
def get_today_hot_datas(content_type):
    today = timezone.now().date()
    read_details = ReadDetail.objects.filter(content_type=content_type, date=today). \
                                            order_by("-read_num")  # 以read_num倒序
    return read_details[:7]    # 切片器，截取前7条数据


# 统计昨日热门点击blog——阅读量前7的blog：
def get_yesterday_hot_datas(content_type):
    today = timezone.now().date()
    yesterday = today - datetime.timedelta(days = 1)
    read_details = ReadDetail.objects.filter(content_type=content_type, date=yesterday). \
                                            order_by("-read_num")  # 以read_num倒序
    return read_details[:7]    # 切片器，截取前7条数据
