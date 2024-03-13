from django.apps import AppConfig
import django.utils.translation as translation


class DownloadConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "download"
    verbose_name = translation.gettext_lazy("Загрузки")


__all__ = []
