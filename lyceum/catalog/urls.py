from django.urls import path, re_path, register_converter

from . import views


class PositiveIntegerConverter:
    regex = r'\d+'

    def to_python(self, value):
        number = int(value)
        if number <= 0:
            raise ValueError("Number must be a positive integer")
        return number

    def to_url(self, value):
        return str(value)


register_converter(PositiveIntegerConverter, 'positive_int')


urlpatterns = [
    path("", views.item_list),
    path("<int:pk>/", views.item_detail),
    re_path(r"^re/(?P<number>\d+)/$", views.catalog_regex),
    path("converter/<positive_int:number>/", views.catalog_converter),
]
