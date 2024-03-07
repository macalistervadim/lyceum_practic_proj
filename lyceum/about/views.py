import django.shortcuts


def description(request):
    template = "about/about.html"
    return django.shortcuts.render(request, template)


__all__ = []
