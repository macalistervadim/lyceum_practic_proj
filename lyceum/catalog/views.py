from django.http import HttpResponse


def item_list(request):
    return HttpResponse("<body>Список элементов</body>")


def item_detail(request, pk):
    return HttpResponse("<body>Подробно элемент</body>")


def catalog_regex(request, number):
    return HttpResponse(f"<body>{number}</body>")


def catalog_converter(request, number):
    return HttpResponse(f"<body>{number}</body>")
