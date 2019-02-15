#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Administrator
#
# Created:     08/02/2019
# Copyright:   (c) Administrator 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------

'''
#A original concept.

from django.http import HttpResponse

def hello(request):
    return HttpResponse("Hello world !")
'''
from django.shortcuts import render
from django.http import HttpResponse
from . import db_tools
from . import server_tools
import json

def hello(request):
    context = {}
    context['hello'] = 'Hello World'
    return render(request, 'hello.htm', context)

def budget(request):
    #records = db_tools.display(request)
    #return render(request, 'budget.htm', {'records':records})
    return render(request, 'budget.htm', {})

def retBills_json(request):
    form = server_tools.checkRequestForm(request)
    totalNum, records = db_tools.get_bills(form["pageSize"], form["pageNumber"], form["sortOrder"])
    ret = {"total":totalNum, "rows": records}
    return HttpResponse(json.dumps(ret, ensure_ascii = False))

def retBillDetails(request):
    d = {
        "date":"2018-2-2",
        "time":"23:12:34",
        "amount":"2.2",
        "comment":"fun",
        "readonly":"true",
    }
    form = server_tools.checkRequestForm(request)
    bill = db_tools.get_bill(id = form["id"], date = form["date"], time = form["time"]);
    billRecord = {}
    billRecord['date'] = bill.datetime.strftime("%Y-%m-%d")
    billRecord['time'] = bill.datetime.strftime("%H:%M:%S")
    billRecord['amount'] = "%.2f" % float(bill.amount)
    billRecord['comment'] = bill.comment
    billRecord['effective_to_date'] = bill.effective_to_date.strftime("%Y-%m-%d")
    billRecord['readonly'] = form["readonly"]
    return render(request, 'billDetails.htm', billRecord)

def addBill(request):
    form = server_tools.checkRequestForm(request)
    if(db_tools.add_bill(request, form)):
        bill = db_tools.get_bill(id = form["id"], date = form["date"], time = form["time"]);
        billRecord = {}
        billRecord['id'] = bill.id
        billRecord['date'] = bill.datetime.strftime("%Y-%m-%d")
        billRecord['time'] = bill.datetime.strftime("%H:%M:%S")
        billRecord['amount'] = "%.2f" % float(bill.amount)
        billRecord['comment'] = bill.comment
        billRecord['effective_to_date'] = bill.effective_to_date.strftime("%Y-%m-%d")
        return HttpResponse(json.dumps(billRecord, ensure_ascii = False))
    else:
        return HttpResponse("false")

def editBill(request):
    '''
    Modify a record of bill.

    a "mode" param is needed in request.
    "mode" takes two value:"read"(default) "edit" "del"
    Nothing's gonna take place when "mode" is not provided.
    '''

    #some authentication checking goes here
    form = server_tools.checkRequestForm(request)
    if(form["mode"] == "read"):
        return HttpResponse("false")
    if(form["mode"] == "edit"):
        db_tools.update_bill(request, form)
    bill = db_tools.get_bill(id = form["id"], date = form["date"], time = form["time"]);
    billRecord = {}
    billRecord['date'] = bill.datetime.strftime("%Y-%m-%d")
    billRecord['time'] = bill.datetime.strftime("%H:%M:%S")
    billRecord['amount'] = "%.2f" % float(bill.amount)
    billRecord['comment'] = bill.comment
    billRecord['effective_to_date'] = bill.effective_to_date.strftime("%Y-%m-%d")
    return HttpResponse(json.dumps(billRecord, ensure_ascii = False))


def deleteBill(request):
    '''
    Delete a record of bill.
    '''
    #some authentication checking goes here
    form = server_tools.checkRequestForm(request)
    if(db_tools.delete_bill(request, form)):
        return HttpResponse("true")
    else:
        return HttpResponse("false");

def retSpendings_json(request):
    form = server_tools.checkRequestForm(request)
    numRecords, records = db_tools.get_daily_spendings(request, form["period"], sortOrder = form["sortOrder"])
    ret = {}
    ret['total'] = numRecords
    ret['rows'] = records
    return HttpResponse(json.dumps(ret, ensure_ascii = False))

def reComputeDailySpendings(request):
    form = server_tools.checkRequestForm(request)
    db_tools.compute_daily_spendings(request, form["period"])
    numRecords, records = db_tools.get_daily_spendings(request, form["period"], sortOrder = form["sortOrder"])
    ret = {}
    ret['total'] = numRecords
    ret['rows'] = records
    return HttpResponse(json.dumps(ret, ensure_ascii = False))

def main():
    pass

if __name__ == '__main__':
    main()
