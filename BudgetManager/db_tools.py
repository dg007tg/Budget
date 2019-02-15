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

def add_bill(request, fields):
    '''
    fields is a dictionary containing all required info to add a bill
    '''
    if(request.GET['amount'] == "0"):
        return False
    now = datetime.datetime.now()
    dateTime = now.strftime("%Y-%m-%d %H:%M:%S")
    amount = float(fields['amount'])
    comment = fields['comment']
    duration = int(fields['duration'])
    effective_to_date = (now + datetime.timedelta(days = (duration - 1)\
                    )).strftime("%Y-%m-%d")

    #update budget
    p = CurrentFlows(datetime = dateTime, amount = amount, comment = comment,\
                effective_to_date = effective_to_date)
    p.save()
    fields["date"] = now.strftime("%Y-%m-%d")
    fields["time"] = now.strftime("%H:%M:%S")
    #cal dayily spending
    date = now.strftime("%Y-%m-%d")
    spending = functions.cal_day_spending(date)
    try:
        p = DailySpending.objects.get(date = date)
    except DailySpending.DoesNotExist:
        p = DailySpending(date = date, spending = spending)
        p.save()
    else:
        p.spending = spending
        p.save()

    return True

def get_bills(pageSize = 0, pageNum = 0, order = "desc"):
    '''
    @param pageSize: rows in a page
    @param pageNum: number of page
    @param order: sorting order(desc or asc)
    '''
    # 通过objects这个模型管理器的all()获得所有数据行，相当于SQL中的SELECT * FROM
    if(not pageSize or not pageNum):
        if(order is 'asc'):
            records = CurrentFlows.objects.all().order_by("datetime")
        else:
            records = CurrentFlows.objects.all().order_by("-datetime")
    else:
        if(isinstance(pageSize, str)):
            pageSize = int(pageSize)
        if(isinstance(pageNum, str)):
            pageNum = int(pageNum)
        pageNum = pageNum + 1
        start = (pageNum - 1) * pageSize
        end = pageNum * pageSize
        total = CurrentFlows.objects.count()
        end = total if (end > total) else end
        if(order is 'asc'):
            records = CurrentFlows.objects.all().order_by("datetime")[start: end]
        else:
            records = CurrentFlows.objects.all().order_by("-datetime")[start: end]

    #return data
    ret = []
    for var in records:
        line = {}
        line['date'] = var.datetime.strftime("%d/%m/%Y")
        line['time'] = var.datetime.strftime("%H:%M:%S")
        line['amount'] = var.amount
        line['comment'] = var.comment
        line['effective_to_date'] = var.effective_to_date.strftime("%d/%m/%Y")
        line['id'] = var.id
        ret.append(line)
    return total, ret

def get_bill(id = -1, date = 0, time = 0):
    '''
    get bill record by id(allocated by mysql), date with time.

    @param date:a string in format "year-month-day" or python date object
    @param time:a string in format "hours:minutes:seconds" or python time object

    return None if nothing was matched.
    '''
    p = None
    try:
        if(id != -1):
            p = CurrentFlows.objects.get(id = id)
            return p
        if(date != 0 ):
           if(time != 0):
            dateTime = "%s %s" % (date, time)
            print(dateTime)
            p = CurrentFlows.objects.get(datetime = dateTime)
            return p
    except CurrentFlows.DoesNotExist:
        return None
    else:
        if(p):
            return p
        else:
            return None

def update_bill(request, fields):
    '''
    Modify a record of CurrentFlows.
    fields is dictionary where keys are fields of CurrentFlows.
    '''
    bill = get_bill(id = fields["id"], date = fields["date"], time = fields["time"])
    #here define which fields can be modified
    bill.amount = fields["amount"]
    bill.comment = fields["comment"]
    bill.effective_to_date = fields["effective_to_date"]
    bill.save()

    return True

def delete_bill(request, fields):
    '''
    Delete a record of CurrentFlows.
    fields is dictionary where keys are fields of CurrentFlows.
    '''
    bill = get_bill(id = fields["id"], date = fields["date"], time = fields["time"])
    bill.delete()
    return True

def get_daily_spendings(request, period, sortOrder = "desc"):
    '''
    @param period: should be an int. The same means as
        how many rows of datas will be returned.
    @param sortOrder: asc or desc
    '''
    numRecords = period
    total = DailySpending.objects.count()
    numRecords = total if (numRecords > total) else numRecords
    records = DailySpending.objects.all().order_by("-date")[0: numRecords]
    ret = []
    if(sortOrder == "asc"):
        for idx in range(len(records)):
            line = {}
            line['date'] = records[period - idx - 1].date.strftime("%d/%m/%Y")
            line['spending'] = "%.2f" % float(records[period - idx - 1].spending)
            ret.append(line)
    else:
        for record in records:
            line = {}
            line['date'] = records[idx].date.strftime("%d/%m/%Y")
            line['spending'] = "%.2f" % float(records[idx].spending)
            ret.append(line)
    return numRecords, ret

def compute_daily_spendings(request, period):
    '''
    @param days: compute daily spending of recent period days
    '''
    now = datetime.datetime.now()
    for i in range(period):
        date = now - datetime.timedelta(days = i)
        date = date.strftime("%Y-%m-%d")
        spending = functions.cal_day_spending(date)
        try:
            p = DailySpending.objects.get(date = date)
        except DailySpending.DoesNotExist:
            p = DailySpending(date = date, spending = spending)
            p.save()
        else:
            p.spending = spending
            p.save()
    return True

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
