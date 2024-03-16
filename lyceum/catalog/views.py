import django.db
import django.http
import django.shortcuts
import django.utils

import catalog.models


def item_list(request):
    items = catalog.models.Item.objects.published()
    context = {
        "items": items,
    }
    return django.shortcuts.render(request, "catalog/item_list.html", context)


def new_items(request):
    queryset = catalog.models.Item.objects.new_items()
    context = {
        "items": queryset,
        "view_type": "new_items",
    }
    return django.shortcuts.render(
        request,
        "catalog/item_filter_date.html",
        context,
    )


def friday_items(request):
    queryset = catalog.models.Item.objects.friday_items()

    context = {
        "items": queryset[:5],
        "view_type": "friday_items",
    }
    return django.shortcuts.render(
        request,
        "catalog/item_filter_date.html",
        context,
    )


def unverified_items(request):
    queryset = catalog.models.Item.objects.unverified_items()
    context = {
        "items": queryset,
        "view_type": "unverified_items",
    }

    return django.shortcuts.render(
        request,
        "catalog/item_filter_date.html",
        context,
    )


def item_detail(request, pk):
    queryset = catalog.models.Item.objects.gallery_images()

    item = django.shortcuts.get_object_or_404(queryset, pk=pk)
    context = {
        "item": item,
    }
    return django.shortcuts.render(request, "catalog/item.html", context)


__all__ = []
