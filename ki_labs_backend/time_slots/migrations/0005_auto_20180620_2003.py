# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2018-06-20 20:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('time_slots', '0004_auto_20180620_2000'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='calendarusertimeslot',
            unique_together=set([('calendar_user', 'calendar_time_slot')]),
        ),
    ]
