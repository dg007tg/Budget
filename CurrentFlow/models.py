from django.db import models
import datetime

# Create your models here.
class CurrentFlows(models.Model):
    datetime = models.DateTimeField(auto_now_add = False)
    effective_to_date = models.DateField("date")
    amount = models.FloatField("amount", default = 0.0)
    comment = models.TextField("comment", default = "null")

class DailySpending(models.Model):
    date = models.DateField(default = datetime.datetime.now())
    spending = models.FloatField(default = 0.0)

