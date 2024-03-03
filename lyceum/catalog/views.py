import django.db
import django.http
import django.shortcuts

import catalog.models


def item_list(request):
    items = (
        catalog.models.Item.objects.only(
            "category__name",
            "mainimage__image",
            "name",
            "text",
        )
        .select_related("category", "mainimage")
        .prefetch_related(
            django.db.models.Prefetch(
                "tags",
                queryset=catalog.models.Tag.objects.only("name"),
            ),
        )
        .filter(category__is_published=True, is_published=True)
        .order_by("category__name")
    )
    context = {
        "items": items,
    }
    return django.shortcuts.render(request, "catalog/item_list.html", context)


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
