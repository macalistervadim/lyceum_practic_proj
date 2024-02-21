import re

import django.core.exceptions
import django.db


class TimeStampedModel(django.db.models.Model):
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

    class Meta:
        abstract = True

    def __str__(self):
        return self.name[:15]

    def save(self, *args, **kwargs):
        if not self.pk:
            self.clean()
        else:
            old_instance = self.__class__.objects.get(pk=self.pk)
            if old_instance.name != self.name:
                self.clean()

        self.normalized_name = self._formatting_value(self.name)
        super().save(*args, **kwargs)

    def clean(self):
        normalized_name = self._formatting_value(self.name)
        found = self.__class__.objects.filter(
            normalized_name=normalized_name,
        )
        if found and found[0].pk != self.pk:
            raise django.core.exceptions.ValidationError(
                "В ваших исправленных значениях уже есть похожее название",
            )
        self.normalized_name = normalized_name

    def _formatting_value(self, value):
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
