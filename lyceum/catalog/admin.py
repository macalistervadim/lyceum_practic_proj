from django.contrib import admin

import catalog.models


@admin.register(catalog.models.Tag)
class AdminTag(admin.ModelAdmin):
    pass


@admin.register(catalog.models.Category)
class AdminCategory(admin.ModelAdmin):
    pass


@admin.register(catalog.models.Item)
class AdminItem(admin.ModelAdmin):
    list_display = (catalog.models.Item.name,
                    catalog.models.Item.is_published)
    list_editable = (catalog.models.Item.is_published,)
    list_display_links = (catalog.models.Item.name,)
    filter_horizontal = (catalog.models.Item.tags,)
