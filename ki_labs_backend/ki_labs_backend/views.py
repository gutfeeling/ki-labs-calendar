from rest_framework.response import Response
from rest_framework.views import APIView

class WelcomeView(APIView):
    """
    get:
    Returns information about the API.

    ###Response schema
        {
            "name" : Name of the API,
            "version" : Version number of the API,
            "description" : A few lines about what the API can do,
            "documentation" : The relative URL where the API is documented
            }
    """

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
            "documentation" : "/docs/",
            }

        return Response(response)
