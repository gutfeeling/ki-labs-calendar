# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2018-06-20 20:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('time_slots', '0003_auto_20180620_1648'),
    ]

    operations = [
        migrations.RenameField(
            model_name='calendarusertimeslot',
            old_name='calendar_timeslot',
            new_name='calendar_time_slot',
        ),
    ]