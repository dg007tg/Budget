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
from . import settings
from . import db_tools
import datetime
import os

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

'''
*************************************************************
A set of functions to generate graphs in user report
'''
class ReportGraphsManager:
    def __init__(self):
        self.GRAPH_CACHE = os.path.join(settings.STATIC_ROOT, "cache", "UserReportGraphs")
        self.period = datetime.timedelta(minutes = 5)
        self.cache_root = settings.CACHE_ROOT
        self.cache_dirs = ["UserReportGraphs"]
        self.startAutoClearCache()
        self.font={"family":"Times New Roman","weight":"normal","size":23}
        #font size correspond to period
        self.fontSize={"7":23, "30":8, "180":4}

    def genDailySpending(self, user_name, period):
        '''
        Generate daylispending graph of recent period days.
        '''
        def transparent(img):
            #convert pixel with certain value into white
            img = img.convert('RGBA')
            L, H = img.size
            color_0 = (255,255,255,255)#要替换的颜色
            for h in range(H):
                for l in range(L):
                    dot = (l,h)
                    color_1 = img.getpixel(dot)
                    if color_1 == color_0:
                        color_1 = color_1[:-1] + (0,)
                        img.putpixel(dot,color_1)
            return img
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.dates as mdates
        import matplotlib.pyplot as plt
        import PIL.Image as Image
        import os
        file_path = os.path.join(self.GRAPH_CACHE, "%s-dailyspending.png" % (user_name,))
        total, rows = db_tools.get_daily_spendings(user_name, period)
        x = [datetime.datetime.strptime(row["date"], '%d/%m/%Y').date() for row in rows]
        y = [row["spending"] for row in rows]
        plt.axes(axisbg="papayawhip")
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator())
        for name in ['top', 'left', 'right', 'bottom']:
            plt.gca().spines[name].set_visible(False)
        #plt.title("Your Shared Dailyspendings")

        plt.plot(x, y, ls="--", lw=3, color='tan', marker='o', ms=10, mec='#FFDEAD', mfc='#FFDEAD', mew=2)
        plt.tick_params(labelsize = self.fontSize[str(period)])
        plt.xlabel('Date', self.font)
        plt.ylabel('Spending', self.font)
        plt.gcf().autofmt_xdate()
        plt.savefig(file_path)
        img = Image.open(file_path)
        img = transparent(img)
        img.save(file_path)

    def startAutoClearCache(self):
        def clear():
            import os
            for dir in self.cache_dirs:
                path = os.path.join(self.cache_root, self.cache_dirs)
                files = os.listdir(path)
                for file in files:
                    os.remove(file)
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print("%s***********Auto Clearing." % now)

        import sched
        timer = sched.scheduler()
        timer.enter(self.period.seconds, 1, clear)
        print("Self clearing is scheduled.\n")

report_graphs_manager = ReportGraphsManager()
'''
End of graphs generators.
*************************************************************
'''

def runWhenBoost():
    clearCache()
