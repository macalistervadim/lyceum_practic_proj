import django.urls

import download.views

app_name = "download"

urlpatterns = [
    django.urls.re_path(
        r"^(?P<path>.+)$",
        download.views.download,
        name="download_image",
    ),
]


__all__ = []
