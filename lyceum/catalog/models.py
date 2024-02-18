import re
import django.core.exceptions
import django.core.validators
import django.db
import core.models


def validator_for_item_text(value):
    if "превосходно" not in value.lower() and "роскошно" not in value.lower():
        raise django.core.exceptions.ValidationError(
            "Текст должен содержать слово 'превосходно'"
            " или 'роскошно'."
        )


def validator_for_tag_slug(slug):
    regex = r"^[a-zA-Z0-9_-]+$"
    if not re.match(regex, slug):
        raise django.core.exceptions.ValidationError(
            "Слаг должен содержать только цифры, "
            "буквы латиницы, и символы '-', '_'"
        )


class Tag(core.models.TimeStampedModel):
    slug = django.db.models.CharField(
        "слаг",
        max_length=200,
        unique=True,
        validators=[
            validator_for_tag_slug,
        ],
        help_text="Введите слаг для тэга",
    )

    class Meta:
        verbose_name = "тэг"
        verbose_name_plural = "тэги"


class Category(core.models.TimeStampedModel):
    slug = django.db.models.CharField(
        "слаг",
        max_length=200,
        unique=True,
        validators=[
            validator_for_tag_slug,
        ],
        help_text="Введите слаг для категории",
    )
    weight = django.db.models.IntegerField(
        "вес",
        default=100,
        validators=[
            django.core.validators.MinValueValidator(0),
            django.core.validators.MaxValueValidator(32767),
        ],
        help_text="Введите вес",
    )

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"


class Item(core.models.TimeStampedModel):
    category = django.db.models.ForeignKey(
        Category,
        on_delete=django.db.models.CASCADE,
        related_name="items",
        verbose_name="Категория",
        help_text="Выберите категорию",
    )
    tags = django.db.models.ManyToManyField(
        Tag,
        related_name="items",
        verbose_name="Теги",
        help_text="Выберите тэг",
    )
    text = django.db.models.TextField(
        "текст",
        validators=[
            validator_for_item_text,
        ],
        help_text="Введите сообщение",
    )

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"
