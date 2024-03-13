import pathlib
import re
import uuid

import django.core.exceptions
import django.db
import django.dispatch
import django.utils.html
import django.utils.translation as translation
import sorl.thumbnail
import transliterate


ONLY_LETTERS_REGEX = re.compile(r"[^a-z0-9]")


def item_directory_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return pathlib.Path("catalog") / str(instance.item.id) / filename


class TimeStampedModel(django.db.models.Model):
    name = django.db.models.CharField(
        translation.gettext_lazy("название"),
        max_length=150,
        help_text=translation.gettext_lazy(
            "Введите название, максимальная длинна - 150"
        ),
        unique=True,
    )
    is_published = django.db.models.BooleanField(
        translation.gettext_lazy("опубликовано"),
        default=True,
        help_text=translation.gettext_lazy("Дата публикации"),
    )
    normalized_name = django.db.models.CharField(
        translation.gettext_lazy("исправленное значение"),
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
                translation.gettext_lazy("Похожее имя есть в базе данных"),
            )

    @staticmethod
    @django.dispatch.receiver(django.db.models.signals.pre_save)
    def pre_save_handler(sender, instance, **kwargs):
        if issubclass(sender, TimeStampedModel):
            instance.normalized_name = instance._formatting_value()

    def _formatting_value(self):
        try:
            transliterated_name = transliterate.translit(
                self.name.lower(),
                "ru",
                reversed=True,
            )
        except transliterate.exceptions.LanguageDetectionError:
            transliterated_name = self.name.lower()

        char_replace_dict = {
            "v": "b",
            "p": "r",
        }

        for char, replacement in char_replace_dict.items():
            transliterated_name = transliterated_name.replace(
                char,
                replacement,
            )

        return ONLY_LETTERS_REGEX.sub("", transliterated_name)


class AbstractModelImage(django.db.models.Model):
    image = sorl.thumbnail.ImageField(
        upload_to=item_directory_path,
        verbose_name=translation.gettext_lazy("изображение"),
    )

    class Meta:
        abstract = True

    def __str__(self):
        return pathlib.Path(self.image.path).stem

    def get_image_300x300(self):
        return sorl.thumbnail.get_thumbnail(
            self.image,
            "300x300",
            crop="center",
            quality=51,
        )

    def get_image_x1280(self):
        return sorl.thumbnail.get_thumbnail(
            self.image,
            "1280",
            quality=51,
        )

    def image_tmb(self):
        if self.image:
            return django.utils.html.mark_safe(
                f"<img src='{self.get_image_300x300().url}' width='50'>",
            )

        return translation.gettext_lazy("Нет изображения")

    image_tmb.short_description = translation.gettext_lazy("превью")
    image_tmb.allow_tags = True
    image_tmb.field_name = "image_tmb"


__all__ = []
