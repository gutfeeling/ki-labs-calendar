from django.urls import path, re_path

from time_slots.views import CalendarTimeSlotView, CalendarTimeSlotDetailView

urlpatterns = [
    re_path("^$", CalendarTimeSlotView.as_view(),
        name = "calendar_time_slot_view"
        ),
    path(
        "<int:pk>/", view = CalendarTimeSlotDetailView.as_view(),
        name = "calendar_time_slot_detail_view"
        ),
    ]
