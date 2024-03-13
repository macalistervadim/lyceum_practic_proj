import django.apps
import django.utils.translation as translation


class CoreConfig(django.apps.AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
    verbose_name = translation.gettext_lazy("Абстрактные модели")


__all__ = []
