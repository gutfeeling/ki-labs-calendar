from datetime import datetime, time, timedelta

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from time_slots.models import CalendarTimeSlot
from users.models import CalendarUser
from utils.datetime_ops import get_rrule_format

class CalendarUserRelatedField(serializers.RelatedField):

    def to_representation(self, value):

        return "Username: {0}, Type: {1}".format(
            value.username,
            "Interviewer" if value.is_interviewer else "Candidate"
            )

    def to_internal_value(self, data):
        try:
            calendar_user = CalendarUser.objects.get(username = data)
        except CalendarUser.DoesNotExist:
            raise serializers.ValidationError("The username does not exist")

        return calendar_user


class CalendarTimeSlotSerializer(ModelSerializer):

    frequency = serializers.ChoiceField(
        required = False,
        choices = ["DAILY", "WEEKLY", "MONTHLY", "YEARLY"],
        write_only = True,
        style = {"base_template" : "input.html"},
        help_text = (
            "How frequently should this time slot repeat? Valid options are "
            "'DAILY', 'WEEKLY', 'MONTHLY' and 'YEARLY'."
            )
        )
    interval = serializers.IntegerField(
        required = False,
        write_only = True,
        help_text = (
            "Integer. When using 'DAILY' frequency, an interval of 2 means "
            "once every two days, but with 'WEEKLY', it means once every two "
            " weeks."
            )
        )
    until = serializers.DateField(
        required = False,
        write_only = True,
        help_text = (
            "A date formatted as YYYY-MM-DD. The time slot will be repeated "
            "until the end (23:59:59) of this day."
            )
        )

    # Use a custom RelatedField for creator, because we want a custom
    # representation of the creator object in the response.
    # The default style for the RelatedField uses the __str__ method of the
    # related model as the request input. We don't want this. Therefore,
    # we also modify the style to a simple text input.
    creator = CalendarUserRelatedField(queryset = CalendarUser.objects.all(),
        style = {"base_template" : "input.html"},
        help_text = "Username of the creator of this time slot e.g. philipp."
        )

    def validate(self, data):

        start_datetime = data["start_datetime"]
        end_datetime = data["end_datetime"]

        # Check if start_datetime and end_datetime correspond to the beginning
        # of an hour.

        if start_datetime.minute != 0 and start_datetime.second != 0:
            raise serializers.ValidationError(
                "The timeslot should start at the beginning of an hour. "
                "For example, 2018-06-22T17:00:00 is allowed, but "
                "2018-06-22T17:30:00 is not allowed."
                )

        if end_datetime.minute != 0 and end_datetime.second != 0:
            raise serializers.ValidationError(
                "The timeslot should end at the beginning of an hour. "
                "For example, 2018-06-22T17:00:00 is allowed, but "
                "2018-06-22T17:30:00 is not allowed."
                )


        # Check if end_datetime is in the future with respect to start_datetime

        if end_datetime - start_datetime <= timedelta(0):
            raise serializers.ValidationError(
                "End datetime in the past compared to Start datetime "
                "(or same)! End datetime represents the end of a time slot, so "
                "it must be in the future compared to Start datetime."
                )

        # If the time slot repeats, then all rrule related
        # parameters must be present.

        are_rrule_parameters_present = [
            "frequency" in data,
            "interval" in data,
            "until" in data,
            ]

        if len(set(are_rrule_parameters_present)) > 1:
            raise serializers.ValidationError(
                "When specifying recurring time slots, all three paramteres "
                "'frequency', 'interval' and 'until' must be provided."
                )

        return data

    def create(self, validated_data):

        are_rrule_parameters_present = [
            "frequency" in validated_data,
            "interval" in validated_data,
            "until" in validated_data,
            ]

        # If none of the rrule parameters are present, then the time slot
        # does not repeat and rrule can be set to null.
        if not(all(are_rrule_parameters_present)):
            validated_data["rrule"] = None
        # If rrule parameters are present, compute the rrule string.
        else:
            validated_data["until"] = datetime.combine(
                validated_data["until"],
                time(hour = 23, minute = 59, second = 59)
                )
            rrule = "FREQ={0};INTERVAL={1};UNTIL={2}".format(
                validated_data["frequency"],
                validated_data["interval"],
                get_rrule_format(validated_data["until"])
                )
            validated_data["rrule"] = rrule

            # The model does not have fields for frequency, interval and
            # until separately, but rather a field for the rrule string.
            # We get rid of these unnecessary fields before saving the
            # model object.
            validated_data.pop("frequency")
            validated_data.pop("interval")
            validated_data.pop("until")

        return CalendarTimeSlot.objects.create(**validated_data)

    class Meta:
        model = CalendarTimeSlot
        fields = "__all__"
        read_only_fields = ("rrule",)
