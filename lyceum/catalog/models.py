import pathlib
import uuid

import django.contrib
import django.core.exceptions
import django.core.validators
import django.db
import django.utils
import tinymce.models

import catalog.models
import catalog.validators
import core.models


def item_directory_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return pathlib.Path("catalog") / str(instance.item.id) / filename


class ItemManager(django.db.models.Manager):
    def published(self):
        oredered_field_item_category = catalog.models.Item.category.field.name
        ordered_field_category_name = catalog.models.Category.name.field.name
        publish = self.get_queryset().filter(
            is_published=True,
            category__is_published=True,
        )
        order_by = publish.order_by(
            f"{oredered_field_item_category}__{ordered_field_category_name}",
            catalog.models.Item.name.field.name,
        )
        select_related = order_by.select_related(
            oredered_field_item_category,
            catalog.models.Item.mainimage.related.name,
        )
        prefetch_related = select_related.prefetch_related(
            django.db.models.Prefetch(
                catalog.models.Item.tags.field.name,
                queryset=catalog.models.Tag.objects.filter(
                    is_published=True,
                ).only(
                    catalog.models.Tag.name.field.name,
                ),
            ),
        )
        return prefetch_related.only(
            catalog.models.Item.name.field.name,
            catalog.models.Item.text.field.name,
            catalog.models.Item.mainimage.related.name,
            f"{oredered_field_item_category}__"
            f"{ordered_field_category_name}",
        )

    def on_main(self):
        return (
            self.published()
            .filter(
                is_on_main=True,
            )
            .order_by(
                catalog.models.Item.name.field.name,
            )
        )


class Tag(core.models.TimeStampedModel):
    slug = django.db.models.SlugField(
        "слаг",
        max_length=200,
        help_text="Введите слаг для тэга, максимальная длинна - 200",
    )

    class Meta:
        ordering = ("name",)
        verbose_name = "тег"
        verbose_name_plural = "теги"


class Category(core.models.TimeStampedModel):
    slug = django.db.models.SlugField(
        "слаг",
        max_length=200,
        help_text="Введите слаг для тэга, максимальная длинна - 200",
    )
    weight = django.db.models.IntegerField(
        "вес",
        default=100,
        validators=[
            django.core.validators.MinValueValidator(1),
            django.core.validators.MaxValueValidator(32767),
        ],
        help_text="Введите вес (от 1 до 32767)",
    )

    class Meta:
        ordering = ("name",)
        verbose_name = "категория"
        verbose_name_plural = "категории"


class Item(core.models.TimeStampedModel):
    objects = ItemManager()

    created = django.db.models.DateTimeField(
        "дата создания",
        auto_now_add=True,
        null=True,
    )
    updated = django.db.models.DateTimeField(
        "последнее изменение",
        auto_now=True,
        null=True,
    )
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
        help_text=(
            "Введите сообщение с содержанием следующих слов: "
            "превосходно/роскошно"
        ),
    )
    is_on_main = django.db.models.BooleanField(
        "для главной",
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
        help_text="Будет приведено к размеру 300x300",
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
        help_text="Будет приведено к размеру 300x300",
    )


class MainImageInline(django.contrib.admin.StackedInline):
    model = MainImage
    extra = 0


class GalleryImageInline(django.contrib.admin.StackedInline):
    model = GalleryImage
    extra = 0


__all__ = []
