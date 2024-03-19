import django.apps
import django.utils.translation as translation


class UsersConfig(django.apps.AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    verbose_name=translation.gettext_lazy("Пользователи")
