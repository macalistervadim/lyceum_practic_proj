import django.conf
import django.contrib
import django.urls
import django.views.i18n

urlpatterns = [
    django.urls.path("admin/", django.contrib.admin.site.urls),
    django.urls.path("", django.urls.include("homepage.urls")),
    django.urls.path("about/", django.urls.include("about.urls")),
    django.urls.path("catalog/", django.urls.include("catalog.urls")),
    django.urls.path("download/", django.urls.include("download.urls")),
    django.urls.path("tinymce/", django.urls.include("tinymce.urls")),
    django.urls.path(
        "set-language/",
        django.views.i18n.set_language,
        name="set_language",
    ),
]

if django.conf.settings.DEBUG:
    import debug_toolbar
    import django.conf.urls.static

    urlpatterns += (
        [
            django.urls.path(
                "__debug__/",
                django.urls.include(debug_toolbar.urls),
            ),
        ]
        + django.conf.urls.static.static(
            django.conf.settings.STATIC_URL,
            document_root=django.conf.settings.STATICFILES_DIRS,
        )
        + django.conf.urls.static.static(
            django.conf.settings.MEDIA_URL,
            document_root=django.conf.settings.MEDIA_ROOT,
        )
    )
