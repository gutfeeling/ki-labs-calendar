from rest_framework.response import Response
from rest_framework.views import APIView

class WelcomeView(APIView):

    def get(self, request, format = None):

        response = {
            "name" : "KI Labs Calendar",
            "version" : "1.0",
            "description" : (
                "A REST calendar API that lets interviewers and candidates "
                "specify time slots when they are available for an interview. "
                "The API can also return time slots when a particular "
                "candidate and a group of interviewers are all available "
                "together."
                ),
            "documentation" : "/docs",
            }

        return Response(response)
