import django.urls

import download.views

app_name = "download"

urlpatterns = [
    django.urls.re_path(
        r"^(?P<path>.+)$",
        download.views.DownloadView.as_view(),
        name="download-image",
    ),
]


__all__ = []
