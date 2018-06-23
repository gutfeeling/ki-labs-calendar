from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from users.models import CalendarUser

class CalendarUserSerializer(ModelSerializer):

    # If we let this class pick up the is_interviewer field automatically from
    # the model, the automatic documentation marks this field as optional.
    # This is wrong. To mark this field as required in the docs, we
    # define this field again in the serializer and set required = True
    # in the serializer field. This leads to the correct behavior in the docs.
    is_interviewer = serializers.BooleanField(
        required = True,
        help_text = (
            "Boolean, accepting values 'true' or 'false'. True if user is an "
            "interviewer, false if user is a candidate"
            )
        )

    class Meta:

        model = CalendarUser
        fields = ("username", "is_interviewer")
