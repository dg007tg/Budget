#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Administrator
#
# Created:     09/02/2019
# Copyright:   (c) Administrator 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from django.http import HttpResponse
from CurrentFlow.models import CurrentFlows, DailySpending
import datetime
from . import view
from . import functions

def add(request):
    if(request.GET['amount'] == "0"):
        return view.budget(request)
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    clock = now.strftime("%H:%M:%S")
    amount = float(request.GET['amount'])
    comment = request.GET['comment']
    duration = int(request.GET['duration'])
    effective_to_date = (now + datetime.timedelta(days = (duration - 1)\
                    )).strftime("%Y-%m-%d")

    #update budget
    p = CurrentFlows(date = date, time = clock, amount = amount, comment = comment,\
                effective_to_date = effective_to_date)
    p.save()
    #cal dayily spending
    spending = functions.cal_day_spending(date)
    try:
        p = DailySpending.objects.get(date = date)
    except DailySpending.DoesNotExist:
        p = DailySpending(date = date, spending = spending)
        p.save()
    else:
        p.spending = spending
        p.save()

    return view.budget(request)

def display(request):
    # 通过objects这个模型管理器的all()获得所有数据行，相当于SQL中的SELECT * FROM
    records = CurrentFlows.objects.all()

    #数据排序
    #CurrentFlows.objects.order_by("-date")

    # 输出所有数据
    ret = []
    for var in records:
        line = {}
        line['date'] = var.date.strftime("%d/%m/%Y")
        line['time'] = var.time.strftime("%H:%M:%S")
        line['amount'] = var.amount
        line['comment'] = var.comment
        line['effective_to_date'] = var.effective_to_date.strftime("%d/%m/%Y")
        ret.append(line)
    return ret

def update(request):
    # 修改其中一个id=1的name字段，再save，相当于SQL中的UPDATE
    test1 = Test.objects.get(id=1)
    test1.name = 'Google'
    test1.save()

    # 另外一种方式
    #Test.objects.filter(id=1).update(name='Google')

    # 修改所有的列
    # Test.objects.all().update(name='Google')

    return HttpResponse("<p>修改成功</p>")

def delete(request):
    # 删除id=1的数据
    test1 = Test.objects.get(id=1)
    test1.delete()

    # 另外一种方式
    # Test.objects.filter(id=1).delete()

    # 删除所有数据
    # Test.objects.all().delete()

    return HttpResponse("<p>删除成功</p>")

def main():
    pass

if __name__ == '__main__':
    main()
