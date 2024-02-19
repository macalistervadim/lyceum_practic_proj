from django.contrib import admin

import catalog.models

LIST_DISPLAY = ("name", "is_published")
LIST_EDITABLE = ("is_published",)
LIST_DISPLAY_LINKS = ("name",)
FILTER_HORIZONTAL = ("tags",)


@admin.register(catalog.models.Tag)
class AdminTag(admin.ModelAdmin):
    list_display = LIST_DISPLAY
    list_editable = LIST_EDITABLE
    list_display_links = LIST_DISPLAY_LINKS


@admin.register(catalog.models.Category)
class AdminCategory(admin.ModelAdmin):
    list_display = LIST_DISPLAY
    list_editable = LIST_EDITABLE
    list_display_links = LIST_DISPLAY_LINKS


@admin.register(catalog.models.Item)
class AdminItem(admin.ModelAdmin):
    list_display = LIST_DISPLAY
    list_editable = LIST_EDITABLE
    list_display_links = LIST_DISPLAY_LINKS
    filter_horizontal = FILTER_HORIZONTAL
