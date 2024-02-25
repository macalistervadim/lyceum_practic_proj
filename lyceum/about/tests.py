import http

import django.test
import django.urls


class AboutPageTest(django.test.TestCase):
    def test_about_page(self):
        url = django.urls.reverse("about:about")
        response = django.test.Client().get(url)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)


__all__ = []
