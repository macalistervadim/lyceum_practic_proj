import django.urls

import catalog.views

app_name = "catalog"


class PositiveIntegerConverter:
    regex = r"\d+"

    def to_python(self, value):
        number = int(value)
        if number <= 0:
            raise ValueError("Number must be a positive integer")
        return number

    def to_url(self, value):
        return str(value)


django.urls.register_converter(PositiveIntegerConverter, "positive_int")


urlpatterns = [
    django.urls.path("", catalog.views.item_list, name="item_list"),
    django.urls.path(
        "<int:pk>/",
        catalog.views.item_detail,
        name="item_detail",
    ),
    django.urls.re_path(
        r"^re/(?P<number>\d+)/$",
        catalog.views.catalog_regex,
        name="catalog_regex",
    ),
    django.urls.path(
        "converter/<positive_int:number>/",
        catalog.views.catalog_converter,
        name="catalog_converter",
    ),
]


__all__ = []
