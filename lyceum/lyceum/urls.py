# -*- coding: utf-8 -*-
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("catalog/", include("catalog.urls")),
    path("about/", include("about.urls")),
]
