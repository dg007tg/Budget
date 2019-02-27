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
    Confirm existens a set of form parameters are provided in request for data.
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
    from . import server_tools
    sessionID = server_tools.sessions.parseCookies(request.COOKIES)
    if(server_tools.sessions.getSession(sessionID) == None):
        ret["user_name"] = None
    else:
        ret["user_name"] = server_tools.sessions.getSession(sessionID).getInfo("user_name")
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
        ret["period"] = int(request.GET['period'])

    return ret

def checkUserRequestForm(request):
    '''
    Confirm existens a set of form parameters are provided in request related to user.
    If not provided, set them to default.

    The request may come from registration or logging in.

    @param request:django request object.

    Return a dictionary where each key-value pair correspond to a form.
    '''
    ret = {}
    ret["user_name"] = None;
    ret["password"] = None;
    ret["email_address"] = None;
    ret["auto_login"] = False;
    if("user_name" in request.POST):
        ret["user_name"] = request.POST["user_name"]
    if("password" in request.POST):
        ret["password"] = request.POST["password"]
    if("email_address" in request.POST):
        ret["email_address"] = request.POST["email_address"]
    if("auto_login" in request.POST):
        ret["auto_login"] = request.POST["auto_login"]

    return ret

'''
*********************************************************
The following is a naive implementation of cookie-session function
'''
class NaiveSession:
    def __init__(self):
        self.sessions = {}
        import datetime
        self.effective_time = datetime.timedelta(minutes = 30)
        self.auto_checking_period = datetime.timedelta(minutes = 5)
        self.startAutoChecking()

    def genSessionID(self):
        '''
        Random id used to distinguish a user.
        '''
        import random, string
        return ''.join(random.sample(string.ascii_letters + string.digits, 9))

    def addSession(self, sessionID, user_info):
        '''
        User_info is the object returned by class method genUserInfoTemplate()
        '''
        if(sessionID not in self.sessions):
            self.sessions[sessionID] = user_info

    def getSession(self, sessionID):
        if(sessionID in self.sessions):
            return self.sessions[sessionID]
        else:
            return None
    def delSession(self, sessionID):
        del self.sessions[sessionID]
    def parseCookies(self, cookies):
        '''
        @param cookies django request.COOKIES obj.
        '''
        return cookies.get("sessionID")

    def setEffectiveTime(timedelta):
        '''
        A session is effective for effective_time.
        @param timedelta: a python datetime.timedelta object
        '''
        self.effective_time = timedelta

    def __del_expired_session(self):
        def strfTime2Datetime(strfTime):
            '''
            Convert a string format time "%Y-%m-%d %H:%M:%S" to a datetime object.
            '''
            tmp = strfTime.split(" ")
            date = list(map(lambda x:int(x),tmp[0].split("-")))
            time = list(map(lambda x:int(x),tmp[1].split(":")))
            return datetime.datetime(date[0],date[1],date[2],time[0],time[1],time[2])

        now = datetime.datetime.now()
        for sessionID, user_info in self.sessions.items():
            last_login_time = strfTime2Datetime(user_info.getInfo("last_login_time"))
            if(((last_login_time + self.effective_time) - now).days < 0):
                delSession(sessionID)
    def startAutoChecking(self):
        import sched
        timer = sched.scheduler()
        timer.enter(self.auto_checking_period.seconds, 1,self.__del_expired_session)
sessions = NaiveSession()
class UserInfo:
    def __init__(self):
        '''
        Define informations correspond to a user that should be saved by a session.
        '''
        self.info = {}
        self.info['user_name'] = None
        self.info['last_login_time'] = None
        self.info['auto_login'] = False

    def setUserInfo(self, key, value):
        '''
        @param obj: object generated by genUserInfoTemplate()(typically a dictionary)
        @param key
        @param value
        @return true if set info successfully false otherwise.
        '''
        if(key in self.info):
            self.info[key] = value
            return True
        else:
            return False
    def getInfo(self, key):
        if(key in self.info):
            return self.info[key]
        else:
            return None
'''
*********************************************************
'''

def main():
    pass

if __name__ == '__main__':
    main()
