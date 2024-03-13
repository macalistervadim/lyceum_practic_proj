from django.apps import AppConfig
import django.utils.translation as translation


class FeedbackConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "feedback"
    verbose_name = translation.gettext_lazy("Обратная связь")


__all__ = []
