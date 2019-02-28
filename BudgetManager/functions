#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:     Define functions of the server.
#
# Author:      Administrator
#
# Created:     11/02/2019
# Copyright:   (c) Administrator 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from CurrentFlow.models import CurrentFlows, DailySpending
import datetime

def cal_day_spending(user_name, date):
    '''
    @param date: either a datetime object or date string
        "year-month-day"
    return : daily consumption
    '''
    #date = datetime.date(2019,2,13)
    if(isinstance(date, str)):
        import re
        match = re.search("(\d{4})-(\d{1,2})-(\d{1,2})", date)
        if(not match):
            return 0.0
        date = datetime.date(int(match.group(1)),\
                    int(match.group(2)),\
                    int(match.group(3)))
    dateTime = datetime.datetime(date.year, date.month, date.day, 23, 59, 59)
    rows = CurrentFlows.objects.filter(user_name = user_name).\
            filter(effective_to_date__gte = date).\
            filter(datetime__lte = dateTime)
    spending = 0.0
    for row in rows:
        start_date = row.datetime.date()
        end_date = row.effective_to_date
        effective_days = (end_date - start_date).days + 1
        amount = float(row.amount)
        spending = spending + amount / effective_days
    return spending

def main():
    pass

if __name__ == '__main__':
    main()
