from django.contrib.auth.models import User
from django.db import models

class CalendarUser(User):

    is_interviewer = models.BooleanField(
        help_text = (
            "Boolean, accepting values 'true' or 'false'. True if user is an "
            "interviewer, false if user is a candidate"
            )
        )

    def __str__(self):
        return "Username: {0}, Type: {1}".format(
            self.username,
            "Interviewer" if self.is_interviewer else "Candidate"
            )
