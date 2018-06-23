from datetime import datetime, timedelta

import coreapi
from rest_framework.schemas import AutoSchema
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from time_slots.models import CalendarTimeSlot
from time_slots.serializers import CalendarTimeSlotSerializer
from users.models import CalendarUser

class CalendarUserTimeSlotAutoSchema(AutoSchema):

    def get_manual_fields(self, path, method):

        extra_fields = []

        if method == "GET":
            extra_fields = [
                coreapi.Field(
                    name = "creator",
                    required = False,
                    location = "query",
                    description = (
                        "Filter by creator. Value should be username."
                        ),
                    )
                ]

        manual_fields = super(
            CalendarUserTimeSlotAutoSchema, self
            ).get_manual_fields(path, method)

        return manual_fields + extra_fields


class CalendarTimeSlotView(generics.ListCreateAPIView):
    """
    get:
    Returns a list of all time slots in the system.

    You can use the optional url query parameter `creator` to filter time slots
    created by a particular user. The value of the query parameter should be
    the username of the user, e.g., `?creator=philipp` or `?creator=carl`.

    ###Response schema
        [
            {
                "id" : Unique ID for the time slot,
                "creator" : The username and type of the creator,
                "start_datetime" : Start of the time slot (YYYY-MM-DDThh:mm:ss),
                "end_datetime" : End of the time slot (YYYY-MM-DDThh:mm:ss),
                "rrule" : Recurrence rule for repeating events, following
                          https://tools.ietf.org/html/rfc5545#section-3.8.5,
                },...
            ]

    post:
    Creates a time slot.

    ###Response schema

        {
            "id" : Unique ID for the created time slot,
            "creator" : The username and type of the creator,
            "start_datetime" : Start of the time slot (YYYY-MM-DDThh:mm:ss),
            "end_datetime" : End of the time slot (YYYY-MM-DDThh:mm:ss),
            "rrule" : Recurrence rule for repeating events, following
                      https://tools.ietf.org/html/rfc5545#section-3.8.5,
            },...
    """

    schema = CalendarUserTimeSlotAutoSchema()

    queryset = CalendarTimeSlot.objects.all()
    serializer_class = CalendarTimeSlotSerializer

    def list(self, request):

        username = request.GET.get("creator", None)

        # If the url query parameter "creator" is not present, return the
        # entire list of users.
        if username is None:
            return super(CalendarTimeSlotView, self).list(request)

        # If the url query paramter "creator" is present, return only the
        # time slots created by that user.
        try:
            creator = CalendarUser.objects.get(username = username)
        except CalendarUser.DoesNotExist:
            return Response(
                {
                    "error" : (
                        "The creator does not exist"
                        ),
                    },
                    status = status.HTTP_400_BAD_REQUEST
                )

        queryset = self.get_queryset()
        queryset = queryset.filter(creator = creator)

        serializer = CalendarTimeSlotSerializer(queryset, many = True)
        return Response(serializer.data)


class CalendarTimeSlotDetailView(generics.RetrieveDestroyAPIView):
    """
    get:
    Returns the details of a time slot.

    ###Response schema

        {
            "id" : Unique ID of the time slot,
            "creator" : The username and type of the creator,
            "start_datetime" : Start of the time slot (YYYY-MM-DDThh:mm:ss),
            "end_datetime" : End of the time slot (YYYY-MM-DDThh:mm:ss),
            "rrule" : Recurrence rule for repeating events, following
                      https://tools.ietf.org/html/rfc5545#section-3.8.5,
            },...

    delete:
    Deletes a time slot.
    """

    queryset = CalendarTimeSlot.objects.all()
    serializer_class = CalendarTimeSlotSerializer


class TimeSlotIntersectionView(APIView):
    """
    get:
    Returns one hour time slots common to two or more users.

    **You must supply the required url query parameter `users` when sending
    requests to this endpoint. The value of the query parameter should be
    a comma separated string of at least two usernames. For example,
    `?users=philipp,carl` will return the time slots common to both philipp
    and carl, while `?users=philipp,sarah,carl` will compute the time slots
    common to all three users.**

    ###Response schema
        [
            {
                "users" : List of users for whom time slot intersections is
                          being computed,
                "intersecting one hour time slots" : [
                    {
                        "start" : Start of a common one hour time slot
                                  (YYYY-MM-DDThh:mm:ss),
                        "end" : End of the common one hour time slot
                                  (YYYY-MM-DDThh:mm:ss),
                        },...
                    ],
                }

            ]

    """

    schema = AutoSchema(
        manual_fields = [
            coreapi.Field(
                name = "users",
                required = True,
                location = "query",
                description = "Comma separated list of usernames.",
                )
            ]
        )

    def get(self, request, format = None):

        usernames_string = request.GET.get("users", None)

        # This endpoint requires a value for the url query parameter "users"

        if usernames_string is None:
            return Response(
                {
                    "error" : (
                        "No users specified. Please specify users using the "
                        "url parameter 'users' e.g. ?users=<user1>,<user2>."
                        ),
                    },
                    status = status.HTTP_400_BAD_REQUEST
                )

        usernames_list = usernames_string.split(",")

        # The url query parameter "user" must be a comma separated list of
        # at least 2 usernames.

        if len(usernames_list) == 1:
            return Response(
                {
                    "error" : (
                        "Only one user specified. Please specify at least two "
                        "users e.g. ?users=<user1>,<user2>."
                        ),
                    },
                    status = status.HTTP_400_BAD_REQUEST
                )

        calendar_users = []

        for username in usernames_list:
            try:
                calendar_user = CalendarUser.objects.get(username = username)
                calendar_users.append(calendar_user)
            except CalendarUser.DoesNotExist:
                return Response(
                    {
                        "error" : (
                            "User {0} does not exist".format(username)
                            ),
                        },
                        status = status.HTTP_400_BAD_REQUEST
                    )

        # Collect sets of all one hour time slots for each user in a list

        one_hour_time_slot_sets = []

        for calendar_user in calendar_users:

            one_hour_time_slot_set_for_this_calendar_user = set()

            calendar_time_slots = CalendarTimeSlot.objects.filter(
                creator = calendar_user
                )

            for calendar_time_slot in calendar_time_slots:
                set_of_all_one_hour_time_slots = set(
                    calendar_time_slot.get_all_one_hour_time_slots()
                    )
                one_hour_time_slot_set_for_this_calendar_user = (
                    one_hour_time_slot_set_for_this_calendar_user.union(
                        set_of_all_one_hour_time_slots
                        )
                    )

            one_hour_time_slot_sets.append(
                one_hour_time_slot_set_for_this_calendar_user
                )

        # Compute the common one hour time slots

        intersecting_one_hour_time_slots  = set.intersection(
            *one_hour_time_slot_sets
            )

        response = {
            "users" : usernames_list,
            "intersecting one hour time slots" : [
                {
                    "start" : dt.ctime(),
                    "end" : (dt + timedelta(hours = 1)).ctime()
                    }
                    for dt in intersecting_one_hour_time_slots
                ]
            }

        return Response(response)
