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


class EndPointCoffeeTest(django.test.TestCase):
    def test_coffee_endpoint(self):
        url = django.urls.reverse("homepage:coffee")
        response = django.test.Client().get(url)
        data = response.content.decode("utf-8")
        self.assertEqual(
            response.status_code,
            http.HTTPStatus.IM_A_TEAPOT,
            "Unexpected status code",
        )
        self.assertEqual(data, "Я чайник", "Incorrect response text")


__all__ = []
