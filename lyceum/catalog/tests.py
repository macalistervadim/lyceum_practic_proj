from django.test import Client, TestCase


class UrlTests(TestCase):
    def test_description(self):
        response = Client().get("/catalog", follow=True)
        self.assertEqual(response.status_code, 200, "Status code != 200")

    def test_item_detail(self):
        response = Client().get("/catalog/1", follow=True)
        self.assertEqual(response.status_code, 200, "Status code != 200")

    def test_catalog_regex(self):
        response = Client().get("/catalog/re/124", follow=True)
        data = response._container[0].decode()
        self.assertIn("124", data, "Page not found this number")

    def test_catalog_converter(self):
        response = Client().get("/catalog/converter/124", follow=True)
        data = response._container[0].decode()
        self.assertIn("124", data, "Page not found this number")
