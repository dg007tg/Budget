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
from django.shortcuts import render, redirect
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
    sessionID = server_tools.sessions.parseCookies(request.COOKIES)
    if(sessionID == None):
        return render(request, 'budget.htm', {"vilidated":False})
    else:
        session = server_tools.sessions.getSession(sessionID)
    return render(request, 'budget.htm', {"validated":True})

def retBills_json(request):
    form = server_tools.checkRequestForm(request)
    sessionID = server_tools.sessions.parseCookies(request.COOKIES)
    session = server_tools.sessions.getSession(sessionID)
    totalNum, records = db_tools.get_bills(session.getInfo("user_name"), form["pageSize"], form["pageNumber"], form["sortOrder"])
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
    sessionID = server_tools.sessions.parseCookies(request.COOKIES)
    session = server_tools.sessions.getSession(sessionID)
    bill = db_tools.get_bill(user_name = session.getInfo("user_name"), id = form["id"], date = form["date"], time = form["time"]);
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
    sessionID = server_tools.sessions.parseCookies(request.COOKIES)
    session = server_tools.sessions.getSession(sessionID)
    if(db_tools.add_bill(request, form)):
        bill = db_tools.get_bill(user_name = session.getInfo("user_name"), id = form["id"], date = form["date"], time = form["time"]);
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
    sessionID = server_tools.sessions.parseCookies(request.COOKIES)
    session = server_tools.sessions.getSession(sessionID)
    if(form["mode"] == "read"):
        return HttpResponse("false")
    if(form["mode"] == "edit"):
        db_tools.update_bill(session.getInfo("user_name"), form)
    bill = db_tools.get_bill(user_name = session.getInfo("user_name"), id = form["id"], date = form["date"], time = form["time"]);
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
    sessionID = server_tools.sessions.parseCookies(request.COOKIES)
    session = server_tools.sessions.getSession(sessionID)
    if(db_tools.delete_bill(session.getInfo("user_name"), form)):
        return HttpResponse("true")
    else:
        return HttpResponse("false");

def retSpendings_json(request):
    form = server_tools.checkRequestForm(request)
    sessionID = server_tools.sessions.parseCookies(request.COOKIES)
    session = server_tools.sessions.getSession(sessionID)
    numRecords, records = db_tools.get_daily_spendings(session.getInfo("user_name"), period = form["period"], sortOrder = form["sortOrder"])
    ret = {}
    ret['total'] = numRecords
    ret['rows'] = records
    return HttpResponse(json.dumps(ret, ensure_ascii = False))

def reComputeDailySpendings(request):
    form = server_tools.checkRequestForm(request)
    sessionID = server_tools.sessions.parseCookies(request.COOKIES)
    session = server_tools.sessions.getSession(sessionID)
    db_tools.compute_daily_spendings(session.getInfo("user_name"), form["period"])
    numRecords, records = db_tools.get_daily_spendings(session.getInfo("user_name"), form["period"], sortOrder = form["sortOrder"])
    ret = {}
    ret['total'] = numRecords
    ret['rows'] = records
    return HttpResponse(json.dumps(ret, ensure_ascii = False))

def registrationDetails(request):
    return render(request, 'registration.htm', {})

def registration(request):
    form = server_tools.checkUserRequestForm(request)
    result = db_tools.add_user(form)
    if(result == 0):
        #successfully add user
        return render(request, 'registrationSuccess.htm', {})
    else:
        return render(request, 'registrationFailure.htm', {})

def login(request):
    sessionID = None
    session = None
    sessionID = server_tools.sessions.parseCookies(request.COOKIES)
    if(sessionID != None):
        session = server_tools.sessions.getSession(sessionID)
    if(session != None):
        print(session.getInfo("auto_login"))
        if(session.getInfo("auto_login")):
            return redirect("user-api/user-report")
    return render(request, 'login.htm', {})

def validate(request):
    form = server_tools.checkUserRequestForm(request)
    ret = db_tools.validate_user(form)
    if(ret == db_tools.PASSWORD_CORRECT):
        response = HttpResponse("0")
        sessionID = None
        session = None
        sessionID = server_tools.sessions.parseCookies(request.COOKIES)
        if(sessionID != None):
            session = server_tools.sessions.getSession(sessionID)
        if(session != None):
            sessionID = sessionID
        else:
            server_tools.sessions.genSessionID()
            user_info = server_tools.UserInfo()
            user_info.setUserInfo("user_name", form["user_name"])
            user_info.setUserInfo("auto_login", form["auto_login"])
            import datetime
            user_info.setUserInfo("last_login_time", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            server_tools.sessions.addSession(sessionID,user_info)

        response.set_cookie("sessionID",sessionID)
        return response
    elif(ret == db_tools.USER_NOT_EXIST):
        return HttpResponse("-1")
    elif(ret == db_tools.PASSWORD_WRONG):
        return HttpResponse("-2")


def main():
    pass

if __name__ == '__main__':
    main()
