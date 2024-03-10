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
    template = "homepage/echo.html"
    if request.method == "POST":
        form = homepage.forms.EchoForm()
        context = {
            "form": form,
        }
        return django.shortcuts.render(request, template, context)

    return django.http.HttpResponseNotAllowed(["POST"])


def submit_echo(request):
    if request.method == "POST":
        form = homepage.forms.EchoForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data["text"]
            return django.http.HttpResponse(text, content_type="text/plain")

    return django.http.HttpResponseNotAllowed(["POST"])


__all__ = []
