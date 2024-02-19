from http import HTTPStatus

from django.test import Client, TestCase


class HomePageTest(TestCase):
    def test_home_page(self):
        response = Client().get("/")
        self.assertEqual(
            response.status_code,
            HTTPStatus.OK,
            "Status code is not 200",
        )


class EndPontCoffeeTest(TestCase):
    def test_coffee_endpoint(self):
        response = Client().get("/coffee/")
        self.assertEqual(
            response.status_code,
            HTTPStatus.IM_A_TEAPOT,
            "Unexpected status code"
        )
