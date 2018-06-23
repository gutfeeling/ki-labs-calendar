from django.conf.urls import url

from time_slots.views import CalendarTimeSlotView

urlpatterns = [
    url(
        regex = "^$",
        view = CalendarTimeSlotView.as_view(),
        name = "calendar_time_slot_view"
        ),
    ]
