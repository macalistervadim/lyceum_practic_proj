from django.test import TestCase, Client


class CatalogPageTest(TestCase):
    def test_catalog_page(self):
        response = Client().get('/catalog/')
        self.assertEqual(response.status_code, 200)
