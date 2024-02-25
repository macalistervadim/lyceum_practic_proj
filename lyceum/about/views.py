import django.shortcuts


def description(request):
    template = "about/about.html"
    context = {}
    return django.shortcuts.render(request, template, context)
