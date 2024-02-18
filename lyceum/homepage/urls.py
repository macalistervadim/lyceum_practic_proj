from django.urls import path

from homepage.views import home, endpoint


urlpatterns = [
    path("", home),
    path("coffee/", endpoint),
]
