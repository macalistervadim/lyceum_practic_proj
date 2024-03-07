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
    new_items = catalog.models.Item.objects.get_new_items()
    context = {
        "items": new_items,
        "view_type": "new_items",
    }
    return django.shortcuts.render(
        request, "catalog/item_filter_date.html", context,
    )


def friday_items(request):
    friday_items = catalog.models.Item.objects.get_friday_items()
    context = {
        "items": friday_items,
        "view_type": "friday_items",
    }
    return django.shortcuts.render(
        request, "catalog/item_filter_date.html", context,
    )


def unverified_items(request):
    unverified_items = catalog.models.Item.objects.get_unverified_items()
    context = {
        "items": unverified_items,
        "view_type": "unverified_items",
    }
    return django.shortcuts.render(
        request, "catalog/item_filter_date.html", context,
    )


def item_detail(request, pk):
    item = django.shortcuts.get_object_or_404(
        catalog.models.Item.objects_item_detail, pk=pk,
    )
    main_image = item.mainimage if hasattr(item, "mainimage") else None
    context = {
        "item": item,
        "main_image": main_image,
    }
    return django.shortcuts.render(request, "catalog/item.html", context)


__all__ = []
