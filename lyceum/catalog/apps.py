import django.apps
import django.utils.translation as translation


class CatalogConfig(django.apps.AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "catalog"
    verbose_name = translation.gettext_lazy("Каталог")


__all__ = []
