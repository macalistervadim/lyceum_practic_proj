from django.test import Client, TestCase


class CatalogPageTest(TestCase):
    def test_catalog_page(self):
        response = Client().get("/catalog/")
        self.assertEqual(response.status_code, 200)
