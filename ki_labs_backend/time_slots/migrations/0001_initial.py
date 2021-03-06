# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2018-06-20 15:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CalendarTimeSlot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_hour', models.IntegerField()),
                ('end_hour', models.IntegerField()),
                ('start_date', models.DateField()),
                ('rrule', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CalendarUserTimeSlot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calendar_timeslot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='time_slots.CalendarTimeSlot')),
            ],
        ),
    ]
