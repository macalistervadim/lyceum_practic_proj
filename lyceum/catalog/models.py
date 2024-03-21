import django.contrib
import django.core.exceptions
import django.core.validators
import django.db
import django.utils
import django.utils.translation as translation
import tinymce.models

import catalog.managers
import catalog.models
import catalog.validators
import core.models


class Tag(core.models.TimeStampedModel):
    slug = django.db.models.SlugField(
        translation.gettext_lazy("слаг"),
        max_length=200,
        help_text=translation.gettext_lazy(
            "Введите слаг для тэга, максимальная длинна - 200",
        ),
    )

    class Meta:
        ordering = ("name",)
        verbose_name = translation.gettext_lazy("тег")
        verbose_name_plural = translation.gettext_lazy("теги")


class Category(core.models.TimeStampedModel):
    slug = django.db.models.SlugField(
        translation.gettext_lazy("слаг"),
        max_length=200,
        help_text=translation.gettext_lazy(
            "Введите слаг для тэга, максимальная длинна - 200",
        ),
    )
    weight = django.db.models.IntegerField(
        translation.gettext_lazy("вес"),
        default=100,
        validators=[
            django.core.validators.MinValueValidator(1),
            django.core.validators.MaxValueValidator(32767),
        ],
        help_text=translation.gettext_lazy("Введите вес (от 1 до 32767)"),
    )

    class Meta:
        ordering = ("name",)
        verbose_name = translation.gettext_lazy("категория")
        verbose_name_plural = translation.gettext_lazy("категории")


class Item(core.models.TimeStampedModel):
    objects = catalog.managers.ItemManager()

    created = django.db.models.DateTimeField(
        translation.gettext_lazy("дата создания"),
        auto_now_add=True,
        null=True,
    )
    updated = django.db.models.DateTimeField(
        translation.gettext_lazy("последнее изменение"),
        auto_now=True,
        null=True,
    )
    category = django.db.models.ForeignKey(
        Category,
        on_delete=django.db.models.CASCADE,
        related_name="items",
        related_query_name="item",
        verbose_name=translation.gettext_lazy("категория"),
        help_text=translation.gettext_lazy("Выберите категорию"),
    )
    tags = django.db.models.ManyToManyField(
        Tag,
        related_name="items",
        verbose_name=translation.gettext_lazy("теги"),
        help_text=translation.gettext_lazy("Выберите тэг"),
    )
    text = tinymce.models.HTMLField(
        translation.gettext_lazy("текст"),
        validators=[
            catalog.validators.ValidateMustContain(
                "превосходно",
                "роскошно",
            ),
        ],
        help_text=(
            translation.gettext_lazy(
                "Введите сообщение с содержанием следующих слов: "
                "превосходно/роскошно",
            )
        ),
    )
    is_on_main = django.db.models.BooleanField(
        translation.gettext_lazy("отображать для главной"),
        default=False,
    )

    class Meta:
        ordering = ("name",)
        verbose_name = translation.gettext_lazy("товар")
        verbose_name_plural = translation.gettext_lazy("товары")


class MainImage(core.models.AbstractModelImage):
    item = django.db.models.OneToOneField(
        Item,
        on_delete=django.db.models.CASCADE,
        related_name="main_image",
        related_query_name="main_image",
    )


class GalleryImage(core.models.AbstractModelImage):
    item = django.db.models.ForeignKey(
        Item,
        on_delete=django.db.models.CASCADE,
        related_name="gallery_images",
        related_query_name="gallery_image",
    )


class MainImageInline(django.contrib.admin.StackedInline):
    model = MainImage
    extra = 0


class GalleryImageInline(django.contrib.admin.StackedInline):
    model = GalleryImage
    extra = 0


__all__ = []
