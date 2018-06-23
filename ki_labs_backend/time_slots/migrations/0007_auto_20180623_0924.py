# Generated by Django 2.0.6 on 2018-06-23 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20180622_1218'),
        ('time_slots', '0006_auto_20180621_1454'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendartimeslot',
            name='end_datetime',
            field=models.DateTimeField(help_text='The end of the time slot, expressed as a datetime formatted as YYYY-MM-DDThh:mm:ss e.g. 2018-06-22T17:00:00. Time slots must end at the beginning of an hour. For example, 2018-06-22T17:00:00 is valid, but 2018-06-22T17:30:00 is not.'),
        ),
        migrations.AlterField(
            model_name='calendartimeslot',
            name='rrule',
            field=models.TextField(help_text='Recurrence rule for repeating time slots, in accordance with https://tools.ietf.org/html/rfc5545#section-3.8.5. Supports only FREQ, INTERVAL and UNTIL keywords for the time being.', null=True),
        ),
        migrations.AlterField(
            model_name='calendartimeslot',
            name='start_datetime',
            field=models.DateTimeField(help_text='The start of the time slot, expressed as a datetime formatted as YYYY-MM-DDThh:mm:ss e.g. 2018-06-22T15:00:00. Time slots must start at the beginning of an hour. For example, 2018-06-22T15:00:00 is valid, but 2018-06-22T15:30:00 is not.'),
        ),
        migrations.AlterUniqueTogether(
            name='calendartimeslot',
            unique_together={('start_datetime', 'end_datetime', 'creator', 'rrule')},
        ),
    ]