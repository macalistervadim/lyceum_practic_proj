import re

import django.core.exceptions
import django.db
import django.dispatch
import django.utils.html
import sorl.thumbnail
import transliterate

ONLY_LETTERS_REGEX = re.compile(r"[^\w]")


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

    @staticmethod
    @django.dispatch.receiver(django.db.models.signals.pre_save)
    def pre_save_handler(sender, instance, **kwargs):
        if issubclass(sender, TimeStampedModel):
            instance.normalized_name = instance._formatting_value()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.normalized_name = self._formatting_value()
        super().save(*args, **kwargs)

    def clean(self):
        self.normalized_name = self._formatting_value()
        if (
            type(self)
            .objects.filter(normalized_name=self.normalized_name)
            .exclude(id=self.id)
            .exists()
        ):
            raise django.core.exceptions.ValidationError(
                "Похожее имя есть в базе данных",
            )

    def _formatting_value(self):
        try:
            transliterated = transliterate.translit(
                self.name.lower(),
                reversed=True,
            )
        except transliterate.exceptions.LanguageDetectionError:
            transliterated = self.name.lower()

        return ONLY_LETTERS_REGEX.sub(
            "",
            transliterated,
        )


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
