import django.apps
import django.utils.translation as translation


class AboutConfig(django.apps.AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "about"
    verbose_name = translation.gettext_lazy("О приложении")


__all__ = []
