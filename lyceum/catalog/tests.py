from http import HTTPStatus

from django.test import Client, TestCase


def check_catalog_regex(func):
    def wrapper(self):
        response = Client().get("/catalog/re/124", follow=True)
        data = response._container[0].decode()
        self.assertIn("124", data, "Page not found this number")
        return func(self)

    return wrapper


def check_catalog_converter(func):
    def wrapper(self):
        response = Client().get("/catalog/converter/124", follow=True)
        data = response._container[0].decode()
        self.assertIn("124", data, "Page not found this number")
        return func(self)

    return wrapper


class UrlTests(TestCase):
    def check_response_status(self, url, expected_status_code):
        response = Client().get(url, follow=True)
        self.assertEqual(
            response.status_code,
            expected_status_code,
            f"Status code != {expected_status_code}",
        )

    def test_description(self):
        self.check_response_status("/catalog", HTTPStatus.OK)

    def test_item_detail(self):
        self.check_response_status("/catalog/1", HTTPStatus.OK)
        self.check_response_status("/catalog/-1", HTTPStatus.NOT_FOUND)
        self.check_response_status("/catalog/string", HTTPStatus.NOT_FOUND)

    @check_catalog_regex
    def test_catalog_regex(self):
        self.check_response_status("/catalog/re/124", HTTPStatus.OK)
        self.check_response_status("/catalog/re/124abs", HTTPStatus.NOT_FOUND)
        self.check_response_status("/catalog/re/-123", HTTPStatus.NOT_FOUND)

    @check_catalog_converter
    def test_catalog_converter(self):
        self.check_response_status("/catalog/converter/124", HTTPStatus.OK)
        self.check_response_status(
            "/catalog/converter/124abs", HTTPStatus.NOT_FOUND
        )
        self.check_response_status(
            "/catalog/converter/-123", HTTPStatus.NOT_FOUND
        )
