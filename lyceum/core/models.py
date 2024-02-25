import re

import django.core.exceptions
import django.db
import django.utils.html
import sorl.thumbnail


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

    def clean(self):
        normalized_name = self._formatting_value(self.name)
        found = self.__class__.objects.exclude(pk=self.pk).filter(
            normalized_name=normalized_name,
        )
        if found.exists():
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


class AbstractModelImage(django.db.models.Model):
    class Meta:
        abstract = True

    def __str__(self):
        return f"Картинка для {self.item}"

    def get_image_300x300(self):
        return sorl.thumbnail.get_thumbnail(
            self.image,
            "300x300",
            crop="center",
            quality=51,
        )

    def image_tmb(self):
        if self.image:
            return django.utils.html.mark_safe(
                f"<img src='{self.get_image_300x300().url}' width='50'>",
            )
        return "Нет изображения"

    image_tmb.short_description = "превью"
    image_tmb.allow_tags = True


__all__ = []
