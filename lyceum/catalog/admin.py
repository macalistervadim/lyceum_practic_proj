import django.contrib
import django_summernote.admin

import catalog.models


@django.contrib.admin.register(catalog.models.Tag)
class AdminTag(django.contrib.admin.ModelAdmin):
    list_display = (catalog.models.Tag.name.field.name,)


@django.contrib.admin.register(catalog.models.Category)
class AdminCategory(django.contrib.admin.ModelAdmin):
    list_display = (catalog.models.Category.name.field.name,)


@django.contrib.admin.register(catalog.models.Item)
class AdminItem(django_summernote.admin.SummernoteModelAdmin):
    summernote_fields = (catalog.models.Item.text.field.name,)
    inlines = [
        catalog.models.MainImageInline,
        catalog.models.GalleryImageInline,
    ]
    list_display = (
        catalog.models.Item.name.field.name,
        catalog.models.Item.is_published.field.name,
    )
    list_editable = (catalog.models.Item.is_published.field.name,)
    list_display_links = (catalog.models.Item.name.field.name,)
    filter_horizontal = (catalog.models.Item.tags.field.name,)


__all__ = []
