import django.urls

import catalog.views

app_name = "catalog"


class PositiveIntegerConverter:
    regex = r"\d*[1-9]\d*"

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
    django.urls.path(
        "converter-item/<positive_int:number>/",
        catalog.views.item_detail,
        name="catalog_converter",
    ),
    django.urls.re_path(
        r"^re/(?P<number>\d*[1-9]\d*)/$",
        catalog.views.item_detail,
        name="catalog_regex",
    ),
    django.urls.path(
        "friday-items/",
        catalog.views.friday_items,
        name="friday_items",
    ),
    django.urls.path(
        "new-items/",
        catalog.views.new_items,
        name="new_items",
    ),
    django.urls.path(
        "unverified-items/",
        catalog.views.unverified_items,
        name="unverified_items",
    ),
]


__all__ = []
