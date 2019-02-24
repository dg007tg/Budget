from django.db import models
import datetime

# Create your models here.
class CurrentFlows(models.Model):
    user_name = models.TextField("user_name", default = "null")
    datetime = models.DateTimeField(auto_now_add = False)
    effective_to_date = models.DateField("date")
    amount = models.FloatField("amount", default = 0.0)
    comment = models.TextField("comment", default = "null")

class DailySpending(models.Model):
    user_name = models.TextField("user_name", default = "null")
    date = models.DateField(default = datetime.datetime.now())
    spending = models.FloatField(default = 0.0)

class UserInformation(models.Model):
    user_name = models.TextField("user_name", default = "null")
    password = models.TextField("password", default = "null")
    auto_login = models.BooleanField("auto_log_in", default = False)
    last_login_time = models.DateTimeField("last_login_time")
    email_address = models.TextField("email_address", default = "null")

