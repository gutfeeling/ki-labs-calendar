from datetime import timedelta
import re

from dateutil.rrule import rrulestr
from django.db import models

from utils.datetime_ops import get_rrule_format

class CalendarTimeSlot(models.Model):

    # Add help text
    start_datetime = models.DateTimeField(
        help_text = (
            "The start of the time slot, expressed as a datetime formatted as "
            "YYYY-MM-DDThh:mm:ss e.g. 2018-06-22T15:00:00. Time slots must "
            "start at the beginning of an hour. For example, "
            "2018-06-22T15:00:00 is valid, but 2018-06-22T15:30:00 is not."
            )
        )
    end_datetime = models.DateTimeField(
        help_text = (
            "The end of the time slot, expressed as a datetime formatted as "
            "YYYY-MM-DDThh:mm:ss e.g. 2018-06-22T17:00:00. Time slots must "
            "end at the beginning of an hour. For example, "
            "2018-06-22T17:00:00 is valid, but 2018-06-22T17:30:00 is not."
            )
        )
    rrule = models.TextField(
        null = True,
        help_text = (
            "Recurrence rule for repeating time slots, in accordance with "
            "https://tools.ietf.org/html/rfc5545#section-3.8.5. Supports "
            "only FREQ, INTERVAL and UNTIL keywords for the time being."
            )
        )
    creator = models.ForeignKey(
        "users.CalendarUser", on_delete = models.CASCADE
        )

    def get_all_one_hour_time_slots(self):
        """
        Expand the recurrence rule to get all one hour time slots corresponding
        to this time slot object.

        Output: List of datetime objects marking the beginning of each one
                hour time slots e.g.

            [
                datetime.datetime(2018, 06, 25, 9, 0, 0),
                datetime.datetime(2018, 06, 25, 10, 0, 0),
                datetime.datetime(2018, 06, 27, 9, 0, 0),
                datetime.datetime(2018, 06, 27, 10, 0, 0),...
                ]
        """

        # First, get all one hour time slots corresponding to the single
        # event. If the single event goes on from 9 o clock to 11 o clock,
        # then this should produce to one hour time slots, one starting from
        # 9, and another starting from 10.

        diff = self.end_datetime - self.start_datetime
        diff_in_hours = diff.seconds // 3600

        start_of_one_hour_timeslots = [
            self.start_datetime + timedelta(hours = i)
            for i in range(diff_in_hours)
            ]


        # If the time slot does not repeat, rrule will be null, and there
        # is no need to expand any recurrence relatio.
        if self.rrule is None:
            return start_of_one_hour_timeslots

        # If the event repeats, expand the recurrence relation to get all
        # one hour time slots

        all_one_hour_timeslots = []

        for start in start_of_one_hour_timeslots:
            start_rrule_format = get_rrule_format(start)
            all_one_hour_timeslots += list(
                rrulestr(
                    "DTSTART:{0} RRULE:{1}".format(
                        start_rrule_format, self.rrule
                        )
                    )
                )

        return all_one_hour_timeslots

    def __str__(self):
        return "Start datetime : {0}, End datetime : {1}, RRule : {2}".format(
            self.start_datetime, self.end_datetime, self.rrule
            )

    class Meta:
        # An user should not be able to create the same time slot again and
        # again.
        unique_together = (
            ("start_datetime", "end_datetime", "creator", "rrule"),
            )
