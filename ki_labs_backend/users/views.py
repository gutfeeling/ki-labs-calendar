import coreapi
from rest_framework.schemas import AutoSchema
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from users.models import CalendarUser
from users.serializers import CalendarUserSerializer

class CalendarUserAutoSchema(AutoSchema):

    def get_manual_fields(self, path, method):

        extra_fields = []

        if method == "GET":
            extra_fields = [
                coreapi.Field(
                    name = "type",
                    required = False,
                    location = "query",
                    description = (
                        "Filter by type. Value should be 'interviewer' or "
                        "'candidate'.",
                        ),
                    ),
                ]

        manual_fields = super(CalendarUserAutoSchema, self).get_manual_fields(
            path, method
            )
        return manual_fields + extra_fields


class CalendarUserView(generics.ListCreateAPIView):
    """
    get:
    Returns a list of users in the database.

    You can use the optional url query parameter `type` to filter by
    interviewers or candidates e.g. `?type=interviewer` or `?type=candidate`.

    ###Response schema

        [
            {
                "username" : Username of the user,
                "is_interviewer" : True if user is an interviewer, else False.
                },...
            ]

    post:
    Creates a new user.

    ###Response schema

        {
                "username" : Username of the created user,
                "is_interviewer" : True if the created user is an interviewer,
                                   else False.
            }
    """

    schema = CalendarUserAutoSchema()

    queryset = CalendarUser.objects.all()
    serializer_class = CalendarUserSerializer

    def list(self, request):

        calendar_user_type = request.GET.get("type", None)

        if calendar_user_type is None:
            return super(CalendarUserView, self).list(request)

        elif calendar_user_type == "interviewer":
            queryset = self.get_queryset()
            queryset = queryset.filter(is_interviewer = True)

        elif calendar_user_type == "candidate":
            queryset = self.get_queryset()
            queryset = queryset.filter(is_interviewer = False)

        else:
            return Response(
                {
                    "error" : (
                        "Unknown value for the 'type' url parameter. "
                        "The type paramater must be either 'interviewer' or "
                        "'candidate'."
                        ),
                    },
                    status = status.HTTP_400_BAD_REQUEST
                )

        serializer = CalendarUserSerializer(queryset, many = True)
        return Response(serializer.data)
