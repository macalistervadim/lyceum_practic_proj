from django.contrib import admin

from catalog.models import Tag, Category, Item


admin.site.register(Tag)
admin.site.register(Category)


@admin.register(Item)
class AdminItem(admin.ModelAdmin):
    list_display = ("name", "is_published")
    list_editable = ("is_published",)
    list_display_links = ("name",)
    filter_horizontal = ("tags",)
