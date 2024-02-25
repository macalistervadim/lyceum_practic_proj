from django.contrib import admin

import catalog.models


@admin.register(catalog.models.Tag)
class AdminTag(admin.ModelAdmin):
    list_display = (catalog.models.Tag.name.field.name,)


@admin.register(catalog.models.Category)
class AdminCategory(admin.ModelAdmin):
    list_display = (catalog.models.Category.name.field.name,)


@admin.register(catalog.models.Item)
class AdminItem(admin.ModelAdmin):
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
