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
import json

def hello(request):
    context = {}
    context['hello'] = 'Hello World'
    return render(request, 'hello.htm', context)

def budget(request):
    #records = db_tools.display(request)
    #return render(request, 'budget.htm', {'records':records})
    return render(request, 'budget.htm', {})

def retRecords_json(request):
    records = db_tools.display(request)
    return HttpResponse(json.dumps(records, ensure_ascii = False))

def main():
    pass

if __name__ == '__main__':
    main()
