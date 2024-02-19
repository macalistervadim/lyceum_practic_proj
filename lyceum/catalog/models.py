import re

import django.core.exceptions
import django.core.validators
import django.db
from django.utils.translation import gettext_lazy as _

import core.models


# def validator_for_item_text(value):
#     if "превосходно" not in value.lower() and "роскошно" not in value.lower():
#         raise django.core.exceptions.ValidationError(
#             "Текст должен содержать слово 'превосходно'"
#             " или 'роскошно'.",
#         )


class ValidateMustContain:
    def __init__(self, *words):
        self.words = words

    def __call__(self, value):
        missing_words = [word for word in self.words if word.lower() not in value.lower()]
        if missing_words:
            raise django.core.exceptions.ValidationError(
                _("Следующие слова должны присутствовать в тексте: %(words)s."),
                params={"words": ", ".join(missing_words)},
            )
        return value


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
        verbose_name="категория",
        help_text="Выберите категорию",
    )
    tags = django.db.models.ManyToManyField(
        Tag,
        related_name="items",
        verbose_name="теги",
        help_text="Выберите тэг",
    )
    # text = django.db.models.TextField(
    #     "текст",
    #     validators=[
    #         validator_for_item_text,
    #     ],
    #     help_text="Введите сообщение",
    # )
    text = django.db.models.TextField(
        "текст",
        help_text="Введите сообщение",
    )

    def clean(self):
        validator = ValidateMustContain('превосходно', 'роскошно')
        validator(self.text)

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"
