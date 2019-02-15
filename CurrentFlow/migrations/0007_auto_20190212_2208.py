# Generated by Django 2.1.5 on 2019-02-12 14:08

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('CurrentFlow', '0006_auto_20190212_1530'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='currentflows',
            name='date',
        ),
        migrations.RemoveField(
            model_name='currentflows',
            name='time',
        ),
        migrations.AddField(
            model_name='currentflows',
            name='datetime',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='dailyspending',
            name='date',
            field=models.DateField(default=datetime.datetime(2019, 2, 12, 22, 8, 30, 815064)),
        ),
    ]
