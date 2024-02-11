from django.test import Client, TestCase


class HomePageTest(TestCase):
    def test_home_page(self):
        response = Client().get("/")
        self.assertEqual(response.status_code, 200)
