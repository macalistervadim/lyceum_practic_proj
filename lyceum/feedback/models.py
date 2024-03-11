import django.db


class Feedback(django.db.models.Model):
    text = django.db.models.TextField(
        "текстовое поле",
        help_text="Введите текстовое поле обращения",
    )
    created = django.db.models.DateTimeField(
        "дата создания",
        auto_now_add=True,
        null=True,
        help_text="Дата создания",
    )
    mail = django.db.models.EmailField(
        "электронный адрес",
        help_text="Адрес электронной почты",
    )


__all__ = []
