import django.apps


class RatingConfig(django.apps.AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "rating"
    verbose_name = "Рейтинг"


__all__ = []
