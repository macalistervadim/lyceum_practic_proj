import django.db


class TimeStampedModel(django.db.models.Model):
    id = django.db.models.BigAutoField(
        "id",
        primary_key=True,
        validators=[
            django.core.validators.MinLengthValidator(1),
        ],
        help_text="id",
    )
    name = django.db.models.CharField(
        "название",
        max_length=150,
        help_text="Введите название",
        unique=True,
    )
    is_published = django.db.models.BooleanField(
        "опубликовано",
        default=True,
        help_text="Дата публикации",
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name[:15]
