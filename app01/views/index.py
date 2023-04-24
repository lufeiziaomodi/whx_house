from django.shortcuts import render, redirect, HttpResponse
from django import forms
from app01 import models
from app01.utils.bootstrap import BootStrapForm, BootStrapModelForm
from django.core.exceptions import ValidationError
from app01.utils.encrypt import md5
from django.core import serializers
import datetime

def index_page(request):
    return render(request, "index_page.html")

def index_change(request):
    "修改选择"
    from app01.models import Select
    nid = request.GET.get('nid')
    # http://127.0.0.1:8000/index/index_change?nid=1
    Select.objects.filter(id=1).update(num=nid)
    return redirect("/index")


def index(request):
    from app01.models import HotSearch
    from app01.models import Comment
    from app01.models import SpiderTime
    from app01.models import Select
    from app01.models import Text
    from urllib import parse
    # 选取事件归1
    sel = list(Select.objects.all())
    if sel == []:
        Select(num=1).save()

    # 热搜处理
    hotsearch = HotSearch.objects.order_by('-raw_hot')[0:50]
    url = 'https://s.weibo.com/weibo?q={}'
    url_list=[]
    num =0
    for obj in hotsearch:
        url_list.append(url.format(parse.quote("#"+obj.word+"#")))
        num=num+1
    # 以下均和选取事件相关
    # 评论按地区处理：和选取事件相关
    num =Select.objects.first().num
    comment = Comment.objects.filter(text_word="#"+hotsearch[num-1].word.replace(" ","")+"#")
    data_list = { '北京': 0,'天津': 0,'上海': 0, '重庆': 0, '河北': 0, '河南': 0,'云南': 0,'辽宁': 0,'黑龙江': 0, '湖南': 0,'安徽': 0, '山东': 0,'新疆': 0, '江苏': 0,'浙江': 0,'江西': 0,'湖北': 0,'广西': 0,'甘肃': 0,'山西': 0,'内蒙古': 0,'陕西': 0,'吉林': 0,'福建': 0,'贵州': 0,'广东': 0,'青海': 0,'西藏': 0, '四川': 0,'宁夏': 0, '海南': 0,'中国台湾': 0,'中国香港': 0,'澳门': 0,'南海诸岛': 0}
    data_key=data_list.keys()
    data_key_list=[]
    date_time=[]
    for i in data_key:
        data_key_list.append(i)
    # print(data_key_list)
    for i in comment:
        if i.comment_source in data_key_list:
            # print(i.comment_source)
            data_list[i.comment_source]=data_list[i.comment_source]+1+i.total_num+i.comment_like_num
    #前n条文章获取
    text = Text.objects.filter(text_word="#"+hotsearch[num-1].word.replace(" ","")+"#").order_by('-text_like_num')[0:100]
    # 时间获取：
    ontime =SpiderTime.objects.first()

    new_time_str =datetime.datetime.strptime(ontime.new,"%Y-%m-%d %H:%M:%S")
    time_str= {}
    hour_delta = datetime.timedelta(hours=1)
    for i in range(7):
        tm = new_time_str.strftime('%Y-%m-%d %H')
        time_str[tm]=0
        new_time_str=new_time_str-hour_delta
    for i in comment:
        if i.comment_time[0:13] in time_str:
            # print(i.comment_source)
            time_str[i.comment_time[0:13]]=time_str[i.comment_time[0:13]]+1
    keys = list(time_str.keys())
    values = list(time_str.values())
    keys.reverse()
    key = []
    for i in keys:
        key.append(i[10:13])

    values.reverse()
    time_str=dict(zip(key, values))
    print(time_str)
    return render(request,'index.html',{'hotsearch':hotsearch,'ontime':ontime,'url_list':url_list,'ontime':ontime,'data_list':data_list,'comment':comment,'text':text,"num":num,'time_str':time_str})