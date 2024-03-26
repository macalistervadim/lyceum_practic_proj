import django.urls

import catalog.views

app_name = "catalog"


class PositiveIntegerConverter:
    regex = r"[1-9]\d*"

    def to_python(self, value):
        number = int(value)

        if number <= 0:
            raise ValueError("Number must be a positive integer")

        return number

    def to_url(self, value):
        return str(value)


django.urls.register_converter(PositiveIntegerConverter, "positive_int")


urlpatterns = [
    django.urls.path("", catalog.views.ItemList.as_view(), name="item-list"),
    django.urls.path(
        "<int:pk>/",
        catalog.views.ItemDetail.as_view(),
        name="item-detail",
    ),
    django.urls.path(
        "converter-item/<positive_int:pk>/",
        catalog.views.ItemDetail.as_view(),
        name="catalog-converter",
    ),
    django.urls.re_path(
        r"^re/(?P<pk>\d*[1-9]\d*)/$",
        catalog.views.ItemDetail.as_view(),
        name="catalog-regex",
    ),
    django.urls.path(
        "friday-items/",
        catalog.views.FridayItems.as_view(),
        name="friday-items",
    ),
    django.urls.path(
        "new-items/",
        catalog.views.NewItems.as_view(),
        name="new-items",
    ),
    django.urls.path(
        "unverified-items/",
        catalog.views.UnverifiedItems.as_view(),
        name="unverified-items",
    ),
    django.urls.path(
        "rating/<int:item_id>/delete/",
        catalog.views.RatingDeleteView.as_view(),
        name="delete-rating",
    ),
]


__all__ = []
