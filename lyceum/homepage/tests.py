from http import HTTPStatus

from django.test import Client, TestCase


class HomePageTest(TestCase):
    def test_home_page(self):
        response = Client().get("/")
        self.assertEqual(
            response.status_code, HTTPStatus.OK, "Status code is not 200",
        )


class EndPontCoffeeTest(TestCase):
    def test_endpont_coffee(self):
        response = Client().get("/coffee/")
        self.assertEqual(
            response.status_code,
            HTTPStatus.IM_A_TEAPOT,
            "Status code is not 418",
        )

    def test_coffee_content(self):
        response = Client().get("/coffee/")
        data = response.content.decode()
        self.assertIn("Я чайник", data, "Page not found this text")
