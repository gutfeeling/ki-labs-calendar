from django.urls import re_path, path

from users.views import CalendarUserView, CalendarUserDetailView

urlpatterns = [
    re_path(
        "^$", CalendarUserView.as_view(),
        name = "calendar_user_view"
        ),
    path(
        "<str:username>/", CalendarUserDetailView.as_view(),
        name = "calendar_user_detail_view"
        ),
    ]
