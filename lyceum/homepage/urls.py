from django.urls import path

import homepage.views


urlpatterns = [
    path("", homepage.views.home),
    path("coffee/", homepage.views.endpoint),
]
