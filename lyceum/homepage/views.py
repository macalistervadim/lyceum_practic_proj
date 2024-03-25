import http

import django.contrib.auth.decorators
import django.db.models
import django.http
import django.shortcuts
import django.urls
import django.views
import django.views.generic

import catalog.models
import homepage.forms


class HomeView(django.views.generic.ListView):
    template_name = "homepage/home.html"
    context_object_name = "items"

    def get_queryset(self):
        return catalog.models.Item.objects.on_main()


class EndpointView(django.views.View):
    def get(self, request):
        if request.user.is_authenticated:
            request.user.profile.coffee_count += 1
            request.user.profile.save()

        return django.http.HttpResponse(
            "Я чайник",
            status=http.HTTPStatus.IM_A_TEAPOT,
        )


class EchoView(django.views.View):
    def get(self, request):
        form = homepage.forms.EchoForm()
        context = {"form": form}
        return django.shortcuts.render(request, "homepage/echo.html", context)

    def post(self, request):
        form = homepage.forms.EchoForm(request.POST)
        if form.is_valid():
            return django.http.HttpResponse(form.cleaned_data["text"])

        return django.http.HttpResponseNotAllowed(
            permitted_methods=["POST"],
        )

    # flake8: noqa
    def dispatch(self, request, *args, **kwargs):
        if request.path == django.urls.reverse("homepage:echo_submit"):
            if request.method == "POST":
                return self.post(request, *args, **kwargs)
            elif request.method == "GET":
                return self.get(request, *args, **kwargs)

            return django.http.HttpResponseNotAllowed(
                permitted_methods=["GET", "POST"]
            )

#test

__all__ = []
