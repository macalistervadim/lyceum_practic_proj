import django.http
import django.shortcuts

import catalog.models


def item_list(request):
    template = "catalog/item_list.html"
    items = (
        catalog.models.Item.objects.filter(is_published=True)
        .order_by("category__name", "name")
        .only(
            "name",
            "text",
        )
        .prefetch_related(
            django.db.models.Prefetch(
                "tags",
                queryset=catalog.models.Tag.objects.only("name"),
            ),
        )
    )
    context = {"items": items}
    return django.shortcuts.render(request, template, context)


def item_detail(request, pk):
    template = "catalog/item.html"
    queryset = (
        catalog.models.Item.objects.select_related("category", "mainimage")
        .prefetch_related(
            django.db.models.Prefetch(
                "tags", queryset=catalog.models.Tag.objects.only("name"),
            ),
            "gallery_images",
        )
        .only("name", "text", "category__name")
    )
    item = django.shortcuts.get_object_or_404(queryset, pk=pk)
    main_image = item.mainimage
    gallery_images = item.gallery_images.all()

    main_image_url = get_thumbnail_url(main_image)
    gallery_images_urls = [
        get_thumbnail_url(image) for image in gallery_images
    ]

    context = {
        "item": item,
        "main_image_url": main_image_url,
        "gallery_images_urls": gallery_images_urls,
    }
    return django.shortcuts.render(request, template, context)


def get_thumbnail_url(image):
    if image:
        return image.get_image_300x300().url
    return None


def catalog_regex(request, number):
    return django.http.HttpResponse(f"<body>{number}</body>")


def catalog_converter(request, number):
    return django.http.HttpResponse(f"<body>{number}</body>")


__all__ = []
