import pathlib

import django.conf
import django.http
import django.views


class DownloadView(django.views.View):
    def get(self, request, path):
        return django.http.FileResponse(
            open(django.conf.settings.MEDIA_ROOT / pathlib.Path(path), "rb"),
            as_attachment=True,
        )


__all__ = []
