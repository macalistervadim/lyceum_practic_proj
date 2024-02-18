from django.urls import path

from homepage.views import endpoint, home


urlpatterns = [
    path("", home),
    path("coffee/", endpoint),
]
