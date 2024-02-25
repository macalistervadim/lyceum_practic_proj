import django.http
import django.shortcuts

import catalog.models


def item_list(request):
    template = "catalog/item_list.html"
    items = catalog.models.Item.objects.all()
    context = {"items": items}
    return django.shortcuts.render(request, template, context)


def item_detail(request, pk):
    template = "catalog/item.html"
    item = django.shortcuts.get_object_or_404(
        catalog.models.Item, pk=pk,
    )
    context = {"item": item}
    return django.shortcuts.render(request, template, context)


def catalog_regex(request, number):
    return django.http.HttpResponse(f"<body>{number}</body>")


def catalog_converter(request, number):
    return django.http.HttpResponse(f"<body>{number}</body>")
