from django.test import Client, TestCase


class UrlTests(TestCase):
    def test_description(self):
        response = Client().get("/catalog", follow=True)
        self.assertEqual(response.status_code, 200, "Статус код не 200")

    def test_item_detail(self):
        response = Client().get("/catalog/1", follow=True)
        self.assertEqual(response.status_code, 200, "Статус код не 200")
