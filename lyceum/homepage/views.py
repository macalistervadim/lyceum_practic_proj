import http

import django.db.models
import django.http
import django.shortcuts

import catalog.models
import homepage.forms


def home(request):
    template = "homepage/home.html"
    items = catalog.models.Item.objects.on_main()
    context = {
        "items": items,
    }
    return django.shortcuts.render(request, template, context)


def endpoint(request):
    return django.http.HttpResponse(
        "Я чайник",
        status=http.HTTPStatus.IM_A_TEAPOT,
    )


def echo(request):
    form = homepage.forms.EchoForm(request.POST or None)
    if request.path == django.shortcuts.reverse("homepage:echo_submit"):
        if request.method == "POST" and form.is_valid():
            return django.http.HttpResponse(form.cleaned_data["text"])

        return django.http.HttpResponseNotAllowed(permitted_methods=["POST"])

    if request.method == "GET":
        context = {"form": form}
        return django.shortcuts.render(request, "homepage/echo.html", context)

    return django.http.HttpResponseNotAllowed(permitted_methods=["GET"])


__all__ = []
