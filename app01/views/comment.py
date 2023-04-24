import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from app01 import models
from app01.utils.Snownlp_Analysis import snownlp_anlysis
from app01.utils.cba_emotion import get_cba
from django.core import serializers


def comment_page(request):
    return render(request, "comment.html")


@csrf_exempt
def ciyun(request):
    data_id = request.POST.get("id")
    # 进行从数据库中取数据的操作
    result = {
        "status": True,
        "data": {
            "data_id": data_id
        }
    }
    return JsonResponse(result)


@csrf_exempt
def update(request):
    print("响应成功")
    data_list = models.Emotion.objects.all()
    if data_list:
        models.Emotion.objects.all().delete()
        for i in range(1, 6):
            print(f"第{i}次执行")
            path = "app01/static/form/%d.csv" % i
            pos, neg = snownlp_anlysis(path)
            pos1, neg1 = get_cba(path)
            models.Emotion.objects.create(e_id=i, sum_positive=pos, sum_negtive=neg,
                                          sum_positive1=pos1, sum_negtive1=neg1)
    else:
        for i in range(1, 6):
            print(f"第{i}次执行")
            path = "app01/static/form/%d.csv" % i
            pos, neg = snownlp_anlysis(path)
            pos1, neg1 = get_cba(path)
            models.Emotion.objects.create(e_id=i, sum_positive=pos, sum_negtive=neg,
                                          sum_positive1=pos1, sum_negtive1=neg1)
    print("执行结束")

    result = {
        "status": True,
    }
    return JsonResponse(result)


@csrf_exempt
def snownlp(request):
    if request.method == "GET":
        data_list = [{"value": 1, "name": "积极人数"},
                     {"value": 1, "name": "消极人数"}
                     ]
    else:
        data_id = request.POST.get("id")
        # print(f'data_id: {type(data_id)}')
        data_set = models.Emotion.objects.filter(e_id=int(data_id))
        # print(f'snownlp: {data_set}')
        ans = []
        for row in data_set:
            ans.append(row.sum_positive)
            ans.append(row.sum_negtive)
        # print(f'ans[0]type: {type(ans[0])}')
        pos, neg = ans[0], ans[1]
        print(f'pos ,neg : {pos, neg}')
        data_list = [{"value": pos, "name": "积极人数"},
                     {"value": neg, "name": "消极人数"}
                     ]
    result = {
        "status": True,
        "data": {
            "data_list": data_list
        }
    }
    return JsonResponse(result)


@csrf_exempt
def cbaemotion(request):
    if request.method == "GET":
        data_list = [{"value": 1, "name": "积极人数"},
                     {"value": 1, "name": "消极人数"}
                     ]
    else:
        data_id = request.POST.get("id")
        # print(f'data_id: {type(data_id)}')
        data_set = models.Emotion.objects.filter(e_id=int(data_id))
        # print(f'snownlp: {data_set}')
        ans = []
        for row in data_set:
            ans.append(row.sum_positive1)
            ans.append(row.sum_negtive1)
            # print(f'该行数值为{row}')
        # print(f'ans[0]: {ans[0]}')
        pos, neg = ans[0], ans[1]
        print(f'pos ,neg : {pos, neg}')
        data_list = [{"value": pos, "name": "积极人数"},
                     {"value": neg, "name": "消极人数"}
                     ]
    result = {
        "status": True,
        "data": {
            "data_list": data_list
        }
    }
    return JsonResponse(result)


def event1(request):
    return render(request, "event1.html")


def event2(request):
    return render(request, "event2.html")


def event3(request):
    return render(request, "event3.html")


def event4(request):
    return render(request, "event4.html")


def event5(request):
    return render(request, "event5.html")
