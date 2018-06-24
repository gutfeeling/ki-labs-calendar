"""ki_labs_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import path, re_path, include
from rest_framework.documentation import include_docs_urls

from .views import WelcomeView
from time_slots.views import TimeSlotIntersectionView

urlpatterns = [
    re_path(
        r"^$", WelcomeView.as_view(),
        name = "welcome_view"
        ),
    path("users/", include("users.urls")),
    path("time-slots/", include("time_slots.urls")),
    path(
        "time-slot-intersections/", TimeSlotIntersectionView.as_view(),
        name = "time_slot_intersection_view"
        ),
    path("docs/", include_docs_urls(title = "KI Labs Calendar")),
]
