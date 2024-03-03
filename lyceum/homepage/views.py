import http

import django.db.models
import django.http
import django.shortcuts

import catalog.models


def home(request):
    template = "homepage/home.html"
    items = (
        catalog.models.Item.objects.filter(is_on_main=True)
        .only("name", "text", "category__name")
        .select_related("category")
        .prefetch_related(
            django.db.models.Prefetch(
                "tags", queryset=catalog.models.Tag.objects.only("name"),
            ),
        )
    )

    context = {"items": items}
    return django.shortcuts.render(request, template, context)


def endpoint(request):
    return django.http.HttpResponse(
        "Я чайник",
        status=http.HTTPStatus.IM_A_TEAPOT,
    )


__all__ = []
