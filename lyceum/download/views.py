import pathlib

import django.conf
import django.http


def download(request, path):
    return django.http.FileResponse(
        open(django.conf.settings.MEDIA_ROOT / pathlib.Path(path), "rb"),
        as_attachment=True,
    )


__all__ = []
