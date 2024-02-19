import re

import django.core.exceptions
import django.core.validators
import django.db

import catalog.validators
import core.models


def validator_for_item_text(value):
    russian_words_pattern = re.compile(
        r"\bпревосходно\b|\bроскошно\b",
        re.IGNORECASE,
    )
    if not russian_words_pattern.search(value):
        raise django.core.exceptions.ValidationError(
            "Текст должен содержать слово 'превосходно' или 'роскошно'.",
        )


def validator_for_tag_slug(slug):
    regex = r"^[a-zA-Z0-9_-]+$"
    if not re.match(regex, slug):
        raise django.core.exceptions.ValidationError(
            "Слаг должен содержать только цифры, "
            "буквы латиницы, и символы '-', '_'",
        )


class Tag(core.models.TimeStampedModel):
    slug = django.db.models.CharField(
        "слаг",
        max_length=200,
        unique=True,
        validators=[
            validator_for_tag_slug,
        ],
        help_text="Введите слаг для тега",
    )

    class Meta:
        verbose_name = "тег"
        verbose_name_plural = "теги"


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
            django.core.validators.MinValueValidator(1),
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
        verbose_name="категория",
        help_text="Выберите категорию",
    )
    tags = django.db.models.ManyToManyField(
        Tag,
        related_name="items",
        verbose_name="теги",
        help_text="Выберите тэг",
    )
    text = django.db.models.TextField(
        "текст",
        validators=[
            catalog.validators.ValidateMustContain(
                "превосходно",
                "роскошно",
            ),
        ],
        help_text="Введите сообщение",
    )

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"
