#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:     Defines a set of helping functions for server
#
# Author:      Administrator
#
# Created:     15/02/2019
# Copyright:   (c) Administrator 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------
def checkRequestForm(request):
    '''
    Confirm existens a set of form parameters are provided in request.
    If not provided, set them to default.

    @param request:django request object.

    Return a dictionary where each key-value pair correspond to a form.
    '''
    ret = {}

    #default values correspond to each param
    #id is allocated by mysql
    ret["id"] = -1
    ret["date"] = 0
    ret["time"] = 0
    ret["amount"] = 0.0
    ret["comment"] = "add your notes here."
    ret["effective_to_date"] = 0
    ret["duration"] = 1
    ret["readonly"] = "disabled = \"disabled\""
    #used by:
    #view::retBills_json
    #view::retSpendings_json
    ret["sortOrder"] = "asc"
    ret["pageSize"] = "10"
    ret["pageNumber"] = "0"
    #used by:
    #view::retSpendings_json
    ret["period"] = 30
    #used by:
    #view::editBill
    ret["mode"] = "read"
    if("id" in request.GET):
        ret["id"] = request.GET["id"]

    if("date" in request.GET):
        ret["date"] = request.GET["date"]

    if("time" in request.GET):
        ret["time"] = request.GET["time"]

    if("amount" in request.GET):
        ret["amount"] = float(request.GET["amount"])

    if("comment" in request.GET):
        ret["comment"] = request.GET["comment"]

    if("effective_to_date" in request.GET):
        ret["effective_to_date"] = request.GET["effective_to_date"]

    if("duration" in request.GET):
        ret["duration"] = request.GET["duration"]

    if("mode" in request.GET):
        ret["mode"] =request.GET["mode"]
        if(request.GET['mode'] != "read"):
            ret["readonly"] = ""
    else:
        ret["readonly"] = "disabled = \"disabled\""

    if("sortOrder" in request.GET):
        ret["sortOrder"] = request.GET['sortOrder']

    if("pageSize" in request.GET):
        ret["pageSize"] = request.GET['pageSize']

    if("pageNum" in request.GET):
        ret["pageNumber"] = request.GET['pageNum']

    if('period' in request.GET):
        period = int(request.GET['period'])

    return ret


def main():
    pass

if __name__ == '__main__':
    main()
