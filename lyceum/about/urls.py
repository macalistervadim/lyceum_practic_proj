from django.urls import path

import about.views


urlpatterns = [
    path("", about.views.description),
]
