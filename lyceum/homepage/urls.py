import django.urls

import homepage.views

app_name = "homepage"

urlpatterns = [
    django.urls.path("", homepage.views.home, name="home"),
    django.urls.path("coffee/", homepage.views.endpoint, name="coffee"),
    django.urls.path("echo/", homepage.views.echo, name="echo"),
    django.urls.path(
        "echo/submit/",
        homepage.views.submit_echo,
        name="submit-echo",
    ),
]
