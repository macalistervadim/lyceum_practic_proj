import http

import django.http
import django.shortcuts

import catalog.models


def home(request):
    template = "homepage/home.html"
    items = catalog.models.Item.objects.all()
    context = {"items": items}
    return django.shortcuts.render(request, template, context)


def endpoint(request):
    return django.http.HttpResponse(
        "Я чайник", status=http.HTTPStatus.IM_A_TEAPOT,
    )
