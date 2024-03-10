import re

import django.conf
import django.http


class ReverseRussianMiddleware:
    count = 0

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response: django.http.HttpResponse = self.get_response(request)
        self.__class__.count += 1

        if (
            self.__class__.count % 10 == 0
            and django.conf.settings.DJANGO_ALLOW_REVERSE
        ):
            content = response.content.decode()
            for word in re.finditer(r"\b[а-яё]+\b", content, re.IGNORECASE):
                start = word.start()
                end = word.end()
                content = (
                    content[:start] + content[start:end][::-1] + content[end:]
                )

            response.content = content.encode()

        return response


__all__ = []
