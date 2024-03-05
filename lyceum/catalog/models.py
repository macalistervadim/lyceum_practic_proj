import pathlib
import uuid

import django.contrib
import django.core.exceptions
import django.core.validators
import django.db
import django.utils.html
import django.utils.translation
import tinymce.models

import catalog.validators
import core.models


def item_directory_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return pathlib.Path("catalog") / str(instance.item.id) / filename


class ItemManager(django.db.models.Manager):
    def on_main(self):
        return (
            self.get_queryset()
            .filter(is_on_main=True)
            .only("name", "text", "category__name")
            .select_related("category")
            .prefetch_related(
                django.db.models.Prefetch(
                    "tags",
                    queryset=catalog.models.Tag.objects.only("name"),
                    to_attr="tag_names",
                ),
            )
        )

    def published(self):
        return (
            self.get_queryset()
            .select_related(
                "category",
            )
            .prefetch_related(
                django.db.models.Prefetch(
                    "tags",
                    queryset=catalog.models.Tag.objects.filter(
                        is_published=True,
                    ),
                ),
            )
            .only("category__name", "name", "text")
            .filter(category__is_published=True, is_published=True)
            .order_by("category__name")
        )


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
    objects = ItemManager()

    category = django.db.models.ForeignKey(
        Category,
        on_delete=django.db.models.CASCADE,
        related_name="items",
        related_query_name="item",
        verbose_name="категория",
        help_text="Выберите категорию",
    )
    tags = django.db.models.ManyToManyField(
        Tag,
        related_name="items",
        verbose_name="теги",
        help_text="Выберите тэг",
    )
    text = tinymce.models.HTMLField(
        "текст",
        validators=[
            catalog.validators.ValidateMustContain(
                "превосходно",
                "роскошно",
            ),
        ],
        help_text="Введите сообщение",
    )
    is_on_main = django.db.models.BooleanField(
        default=False,
    )

    class Meta:
        ordering = ("name",)
        verbose_name = "товар"
        verbose_name_plural = "товары"


class MainImage(core.models.AbstractModelImage):
    item = django.db.models.OneToOneField(
        Item,
        on_delete=django.db.models.CASCADE,
    )
    image = django.db.models.ImageField(
        "главное изображение",
        upload_to=item_directory_path,
        help_text="будет приведено к размеру 300x300",
    )


class GalleryImage(core.models.AbstractModelImage):
    item = django.db.models.ForeignKey(
        Item,
        on_delete=django.db.models.CASCADE,
        related_name="gallery_images",
        related_query_name="gallery_image",
    )
    image = django.db.models.ImageField(
        "изображения",
        upload_to=item_directory_path,
        help_text="будет приведено к размеру 300x300",
    )


class MainImageInline(django.contrib.admin.StackedInline):
    model = MainImage
    extra = 0


class GalleryImageInline(django.contrib.admin.StackedInline):
    model = GalleryImage
    extra = 0


__all__ = []
