import django.conf
import django.db


class Status(django.db.models.TextChoices):
    NEW = "получено"
    PENDING = "в обработке"
    COMPLETE = "ответ дан"


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
    name = django.db.models.CharField(
        "имя отправителя",
        null=True,
        max_length=150,
        blank=True,
        help_text="Необязательное поле. Укажите имя отправителя. "
                  "Максимальная длинна - 256 символов.",
    )
    status = django.db.models.CharField(
        choices=Status.choices,
        default=Status.NEW,
        max_length=11,
        verbose_name="статус обработки",
    )

    class Meta:
        verbose_name = "обратная связь"
        verbose_name_plural = "обратные связи"

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
        verbose_name="дата и время изменения",
        help_text="дата и время изменения",
        auto_now_add=True,
        null=True,
    )
    _from = django.db.models.CharField(
        choices=Status.choices,
        db_column="from",
        max_length=11,
        verbose_name="перешло из состояния",
    )
    to = django.db.models.CharField(
        choices=Status.choices,
        max_length=11,
        verbose_name="перешло в состояние",
    )

    class Meta:
        verbose_name = "журнал состояния"
        verbose_name_plural = "журнал состояний"

    def __str__(self) -> str:
        return f"Текущее состояние ({self.id})"


__all__ = []
