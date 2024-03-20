import http

import django.test
import django.urls


class HomePageTest(django.test.TestCase):
    def test_home_page(self):
        url = django.urls.reverse("homepage:home")
        response = django.test.Client().get(url)
        self.assertEqual(
            response.status_code,
            http.HTTPStatus.OK,
            "Status code is not 200",
        )


__all__ = []
