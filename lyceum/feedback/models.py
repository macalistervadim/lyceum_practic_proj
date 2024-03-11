import django.db


class Feedback(django.db.models.Model):
    text = django.db.models.TextField(
        "текстовое поле",
        help_text="Введите текстовое поле обращения",
    )
    created_on = django.db.models.DateTimeField(
        "дата и время создания",
        auto_now_add=True,
        null=True,
        help_text="Дата и время создания",
    )
    mail = django.db.models.EmailField(
        "электронный адрес",
        help_text="Адрес электронной почты",
    )


__all__ = []
