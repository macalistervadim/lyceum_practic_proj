import datetime
import random

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
    week_ago = django.utils.timezone.now() - datetime.timedelta(days=6)
    my_ids = catalog.models.Item.objects.filter(
        created__gte=week_ago,
    ).values_list("id", flat=True)
    if my_ids:
        random_ids = random.sample(list(my_ids), min(len(my_ids), 5))
        new_items = catalog.models.Item.objects.filter(id__in=random_ids).only(
            "name", "text",
        )
    else:
        new_items = []

    return django.shortcuts.render(
        request, "catalog/item_filter_date.html", {"items": new_items},
    )


def friday_items(request):
    my_ids = catalog.models.Item.objects.filter(
        updated__week_day=5,
    ).values_list("id", flat=True)
    if my_ids:
        random_ids = random.sample(list(my_ids), min(len(my_ids), 5))
        new_items = catalog.models.Item.objects.filter(id__in=random_ids).only(
            "name", "text",
        )
    else:
        new_items = []

    return django.shortcuts.render(
        request, "catalog/item_filter_date.html", {"items": new_items},
    )


def unverified_items(request):
    unverified_items = catalog.models.Item.objects.filter(
        created=django.db.models.F("updated"),
    ).only("name", "text")

    return django.shortcuts.render(
        request, "catalog/item_filter_date.html", {"items": unverified_items},
    )


def item_detail(request, pk):
    item = django.shortcuts.get_object_or_404(
        (
            catalog.models.Item.objects.select_related(
                "category",
                "mainimage",
            )
            .prefetch_related(
                django.db.models.Prefetch(
                    "tags",
                    queryset=catalog.models.Tag.objects.only("name").filter(
                        is_published=True,
                    ),
                ),
                "gallery_images",
            )
            .only("category__name", "mainimage__image", "name", "text")
        ),
        pk=pk,
        category__is_published=True,
        is_published=True,
    )
    main_image = item.mainimage if hasattr(item, "mainimage") else None
    context = {
        "item": item,
        "main_image": main_image,
    }
    return django.shortcuts.render(request, "catalog/item.html", context)


def catalog_regex(request, number):
    return django.http.HttpResponse(f"<body>{number}</body>")


def catalog_converter(request, number):
    return django.http.HttpResponse(f"<body>{number}</body>")


__all__ = []
