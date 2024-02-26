import django.apps


class CoreConfig(django.apps.AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
    verbose_name = "Абстрактные модели"


__all__ = []
