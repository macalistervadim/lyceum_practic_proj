import django.contrib

import catalog.models


@django.contrib.admin.register(catalog.models.Tag)
class AdminTag(django.contrib.admin.ModelAdmin):
    list_display = (catalog.models.Tag.name.field.name,)


@django.contrib.admin.register(catalog.models.Category)
class AdminCategory(django.contrib.admin.ModelAdmin):
    list_display = (catalog.models.Category.name.field.name,)


@django.contrib.admin.register(catalog.models.Item)
class AdminItem(django.contrib.admin.ModelAdmin):
    inlines = [
        catalog.models.MainImageInline,
        catalog.models.GalleryImageInline,
    ]
    list_display = (
        catalog.models.Item.name.field.name,
        catalog.models.Item.is_published.field.name,
        catalog.models.Item.is_on_main.field.name,
    )
    list_editable = (
        catalog.models.Item.is_published.field.name,
        catalog.models.Item.is_on_main.field.name,
    )
    list_display_links = (catalog.models.Item.name.field.name,)
    filter_horizontal = (catalog.models.Item.tags.field.name,)


__all__ = []
