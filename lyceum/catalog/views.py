import datetime
import random

import django.db
import django.http
import django.shortcuts
import django.utils

import catalog.models


ITEM_PER_PAGE = 5


def item_list(request):
    items = catalog.models.Item.objects.published()
    context = {
        "items": items,
    }
    return django.shortcuts.render(request, "catalog/item_list.html", context)


def new_items(request):
    one_week_ago = django.utils.timezone.now() - datetime.timedelta(days=7)

    new_items = catalog.models.Item.objects.published().filter(
        created__gte=one_week_ago,
    )
    selected_items = random.sample(
        list(new_items),
        min(len(new_items), ITEM_PER_PAGE),
    )
    context = {
        "items": selected_items,
        "view_type": "new_items",
    }
    return django.shortcuts.render(
        request,
        "catalog/item_filter_date.html",
        context,
    )


def friday_items(request):
    item = catalog.models.Item.objects.published()
    filter_item = item.filter(updated__week_day=6)
    filter_order = catalog.models.Item.updated.field.name
    friday_items = filter_item.order_by(f"-{filter_order}")
    context = {
        "items": friday_items[:5],
        "view_type": "friday_items",
    }
    return django.shortcuts.render(
        request,
        "catalog/item_filter_date.html",
        context,
    )


def unverified_items(request):
    item = catalog.models.Item.objects.on_main()
    time_interval = datetime.timedelta(seconds=1)
    filtered_field = catalog.models.Item.updated.field.name
    created__gte = {
        f"{filtered_field}__gte": django.db.models.F(filtered_field)
        - time_interval,
    }
    created__lte = {
        f"{filtered_field}__lte": django.db.models.F(filtered_field)
        + time_interval,
    }
    filter_item = item.filter(**created__gte, **created__lte)
    unverified_items = filter_item.order_by("?")[:5]
    context = {
        "items": unverified_items,
        "view_type": "unverified_items",
    }

    return django.shortcuts.render(
        request,
        "catalog/item_filter_date.html",
        context,
    )


def item_detail(request, pk):
    image_field_name = catalog.models.GalleryImage._meta.get_field(
        "image",
    ).name
    queryset = catalog.models.Item.objects.published().prefetch_related(
        django.db.models.Prefetch(
            "gallery_images",
            queryset=catalog.models.GalleryImage.objects.only(
                image_field_name,
                catalog.models.GalleryImage.image.field.name,
            ),
        ),
    )

    item = django.shortcuts.get_object_or_404(queryset, pk=pk)
    context = {
        "item": item,
    }
    return django.shortcuts.render(request, "catalog/item.html", context)


__all__ = []
