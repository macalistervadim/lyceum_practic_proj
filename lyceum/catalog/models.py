import django.contrib
import django.core.exceptions
import django.core.validators
import django.db
import django.utils.html

import catalog.validators
import core.models


class Tag(core.models.TimeStampedModel):
    slug = django.db.models.SlugField(
        "слаг",
        max_length=200,
        help_text="Введите слаг для тэга",
    )

    class Meta:
        verbose_name = "тег"
        verbose_name_plural = "теги"


class Category(core.models.TimeStampedModel):
    slug = django.db.models.SlugField(
        "слаг",
        max_length=200,
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


class MainImage(core.models.AbstractModelImage):
    item = django.db.models.OneToOneField(
        Item,
        on_delete=django.db.models.CASCADE,
    )
    image = django.db.models.ImageField(
        "главное изображение",
        upload_to="main_image_items/",
        help_text="будет приведено к размеру 300x300",
    )


class GalleryImage(core.models.AbstractModelImage):
    item = django.db.models.ForeignKey(
        Item,
        on_delete=django.db.models.CASCADE,
        related_name="gallery_images",
    )
    image = django.db.models.ImageField(
        "изображения",
        upload_to="gallery_images_item/",
        help_text="будет приведено к размеру 300x300",
    )


class MainImageInline(django.contrib.admin.StackedInline):
    model = MainImage
    extra = 0


class GalleryImageInline(django.contrib.admin.StackedInline):
    model = GalleryImage
    extra = 0


__all__ = []
