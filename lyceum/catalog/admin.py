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
    list_display = ("name", "is_published",)
    list_editable = ("is_published",)
    list_display_links = ("name",)
    filter_horizontal = ("tags",)
