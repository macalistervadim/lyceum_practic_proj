import django.db
import django.http
import django.shortcuts
import django.utils
import django.views.generic

import catalog.models


class ItemList(django.views.generic.ListView):
    template_name = "catalog/item_list.html"
    context_object_name = "items"

    def get_queryset(self):
        return catalog.models.Item.objects.published()


class NewItems(django.views.generic.ListView):
    template_name = "catalog/item_filter_date.html"
    context_object_name = "items"
    extra_context = {"view_type": "new_items"}

    def get_queryset(self):
        return catalog.models.Item.objects.new_items()


class FridayItems(django.views.generic.ListView):
    template_name = "catalog/item_filter_date.html"
    context_object_name = "items"
    extra_context = {"view_type": "friday_items"}

    def get_queryset(self):
        return catalog.models.Item.objects.friday_items()


class UnverifiedItems(django.views.generic.ListView):
    tempalte_name = "catalog/item_filter_date.html"
    extra_context = {"view_type": "unverified_items"}
    context_object_name = "items"

    def get_queryset(self):
        return catalog.models.Item.objects.unverified_items()


class ItemDetail(django.views.generic.DetailView):
    template_name = "catalog/item.html"
    context_object_name = "item"

    def get_queryset(self):
        return catalog.models.Item.objects.gallery_images()


__all__ = []
