import re

import django.core.exceptions
import django.db


class TimeStampedModel(django.db.models.Model):
    def formatting_value(self, value):
        similar_chars = {
            "a": "а",
            "o": "о",
            "y": "у",
            "e": "е",
            "c": "с",
            "m": "м",
            "p": "р",
            "t": "т",
            "x": "х",
            "b": "в",
            "k": "к",
            "h": "н",
            "r": "г",
        }
        words = re.findall("[а-яёa-z]+", value.lower())
        new_value = "".join(
            (similar_chars.get(char, char) for char in "".join(words)),
        )
        return new_value

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
    normalized_name = django.db.models.CharField(
        "исправленное значение",
        max_length=150,
        unique=True,
        editable=False,
    )

    def __str__(self):
        return self.name[:15]

    def save(self, *args, **kwargs):
        try:
            self.normalized_name = self.formatting_value(self.name)
            super().save(*args, **kwargs)
        except django.core.exceptions.ValidationError as e:
            if 'normalized_name' in e.error_dict:
                pass  
            else:
                raise e

    def clean(self):
        normalized_name = self.formatting_value(self.name)
        found = self.__class__.objects.filter(
            normalized_name=normalized_name,
        )
        if found:
            raise django.core.exceptions.ValidationError(
                "В ваших исправленных значениях уже есть похожее название",
            )
        self.normalized_name = normalized_name

    class Meta:
        abstract = True
