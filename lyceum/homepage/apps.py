import django.apps
import django.utils.translation as translation


class HomepageConfig(django.apps.AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "homepage"
    verbose_name = translation.gettext_lazy("Домашняя страница")


__all__ = []
