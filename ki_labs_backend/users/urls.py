from django.conf.urls import url

from users.views import CalendarUserView

urlpatterns = [
    url(
        regex = "^$",
        view = CalendarUserView.as_view(),
        name = "calendar_user_view"
        ),
    ]
