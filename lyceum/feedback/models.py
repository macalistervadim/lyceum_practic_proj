import django.conf
import django.db
import django.utils.translation as translation


class Status(django.db.models.TextChoices):
    NEW = translation.gettext_lazy("получено")
    PENDING = translation.gettext_lazy("в обработке")
    COMPLETE = translation.gettext_lazy("ответ дан")


class Feedback(django.db.models.Model):
    text = django.db.models.TextField(
        translation.gettext_lazy("текстовое поле"),
        help_text=translation.gettext_lazy("Введите текстовое поле обращения"),
    )
    created_on = django.db.models.DateTimeField(
        translation.gettext_lazy("дата и время создания"),
        auto_now_add=True,
        null=True,
        help_text=translation.gettext_lazy("Дата и время создания"),
    )
    mail = django.db.models.EmailField(
        translation.gettext_lazy("электронный адрес"),
        help_text=translation.gettext_lazy("Адрес электронной почты"),
    )
    name = django.db.models.CharField(
        translation.gettext_lazy("имя отправителя"),
        null=True,
        max_length=150,
        blank=True,
        help_text=translation.gettext_lazy(
            "Укажите имя отправителя. Максимальная длинна - 256 символов.",
        ),
    )
    status = django.db.models.CharField(
        choices=Status.choices,
        default=Status.NEW,
        max_length=11,
        verbose_name=translation.gettext_lazy("статус обработки"),
    )

    class Meta:
        verbose_name = translation.gettext_lazy("обратная связь")
        verbose_name_plural = translation.gettext_lazy("обратные связи")
        ordering = ("name",)

    def __str__(self) -> str:
        return f"Обратная связь ({self.id})"


class StatusLog(django.db.models.Model):
    user = django.db.models.ForeignKey(
        django.conf.settings.AUTH_USER_MODEL,
        on_delete=django.db.models.SET_NULL,
        null=True,
    )
    feedback = django.db.models.ForeignKey(
        Feedback,
        on_delete=django.db.models.SET_NULL,
        null=True,
    )
    timestamp = django.db.models.DateTimeField(
        verbose_name=translation.gettext_lazy("дата и время изменения"),
        help_text=translation.gettext_lazy("дата и время изменения"),
        auto_now_add=True,
        null=True,
    )
    _from = django.db.models.CharField(
        choices=Status.choices,
        db_column="from",
        max_length=11,
        verbose_name=translation.gettext_lazy("перешло из состояния"),
    )
    to = django.db.models.CharField(
        choices=Status.choices,
        max_length=11,
        verbose_name=translation.gettext_lazy("перешло в состояние"),
    )

    class Meta:
        verbose_name = translation.gettext_lazy("журнал состояния")
        verbose_name_plural = translation.gettext_lazy("журнал состояний")
        ordering = ("user",)

    def __str__(self) -> str:
        return f"Текущее состояние ({self.id})"


__all__ = []
