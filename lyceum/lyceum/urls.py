# -*- coding: utf-8 -*-
import django.conf
import django.contrib
import django.urls

urlpatterns = [
    django.urls.path("admin/", django.contrib.admin.site.urls),
    django.urls.path("", django.urls.include("homepage.urls")),
    django.urls.path("catalog/", django.urls.include("catalog.urls")),
    django.urls.path("about/", django.urls.include("about.urls")),
    django.urls.path("editor/", django.urls.include("django_summernote.urls")),
]

if django.conf.settings.DEBUG:
    import debug_toolbar

    urlpatterns += (
        django.urls.path(
            "__debug__/",
            django.urls.include(debug_toolbar.urls),
        ),
    )
    urlpatterns += django.conf.urls.static.static(
        django.conf.settings.STATIC_URL,
        document_root=django.conf.settings.STATICFILES_DIRS,
    )
    urlpatterns += django.conf.urls.static.static(
        django.conf.settings.MEDIA_URL,
        document_root=django.conf.settings.MEDIA_ROOT,
    )
