import datetime
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from .models import ReadNum, ReadDetail


def read_statistics_once_read(request, obj):
    ct = ContentType.objects.get_for_model(obj)
    key = "%s_%s_read" % (ct.model, obj.pk)
    print('&&&&&&&&&&&&&&&&&&&&&')
    print(ct.model, print(obj.pk))
    # 36   blog None

    if not request.COOKIES.get(key):
        # 总阅读数 +1
        readnum, created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
        readnum.read_num += 1
        readnum.save()

        # 当天阅读数 +1
        date = timezone.now().date()
        readDetail, created = ReadDetail.objects.get_or_create(content_type=ct, object_id=obj.pk, date=date)
        readDetail.read_num += 1
        readDetail.save()
    print('&&&&&&&&&&&&&&&&&&&&&')
    print(key)
    return key  # blog_36_read


def get_seven_days_read_data(content_type):
    today = timezone.now().date()
    # print(today)      #2020-07-31
    dates = []
    read_nums = []
    for i in range(7, 0, -1):
        date = today - datetime.timedelta(days=i)
        # print(date)
        """
        2020-07-24
        2020-07-25
        2020-07-26
        2020-07-27
        2020-07-28
        2020-07-29
        2020-07-30
        """
        dates.append(date.strftime('%m/%d'))
        # print(dates)
        # ['07/24', '07/25', '07/26', '07/27', '07/28', '07/29', '07/30']
        read_details = ReadDetail.objects.filter(content_type=content_type, date=date)
        # print(read_details)
        """
        <QuerySet []>
        <QuerySet []>
        <QuerySet []>
        <QuerySet []>
        <QuerySet []>
        <QuerySet []>
        <QuerySet []>
        """
        result = read_details.aggregate(read_num_sum=Sum('read_num'))
        # print(result)
        """
        {'read_num_sum': None}
        {'read_num_sum': None}
        {'read_num_sum': None}
        {'read_num_sum': None}
        {'read_num_sum': None}
        {'read_num_sum': None}
        {'read_num_sum': None}

        """
        read_nums.append(result['read_num_sum'] or 0)
        """
        [0]
        [0, 0]
        [0, 0, 0]
        [0, 0, 0, 0]
        [0, 0, 0, 0, 0]
        [0, 0, 0, 0, 0, 0]
        [0, 0, 0, 0, 0, 0, 0]
        """
        print(read_nums)

    return dates, read_nums


def get_today_hot_data(content_type):
    # today = timezone.now()
    # print(today)
    # 2020-07-31 03:12:07.560656+00:00
    today = timezone.now().date()
    read_details = ReadDetail.objects.filter(content_type=content_type, date=today).order_by('-read_num')
    # 由大到小
    # print(read_details)
    # < QuerySet[] >

    return read_details[:7]


def get_yesterday_hot_data(content_type):
    today = timezone.now().date()
    yesterday = today - datetime.timedelta(days=1)
    print('-----------------')
    print('yesterday is', yesterday)
    # yesterday is 2020-07-30
    print('-----------------')
    read_details = ReadDetail.objects.filter(content_type=content_type, date=yesterday).order_by('-read_num')
    print(read_details)
    # <QuerySet []>
    return read_details[:7]
