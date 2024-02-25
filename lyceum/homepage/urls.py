from django.urls import path

from homepage.views import endpoint, home

app_name = "homepage"

urlpatterns = [
    path("", home, name="home"),
    path("coffee/", endpoint, name="coffee"),
]
