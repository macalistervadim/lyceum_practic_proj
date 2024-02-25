from django.urls import path

import about.views

app_name = "about"

urlpatterns = [
    path("", about.views.description, name="about"),
]
