from django.test import Client, TestCase


class AboutPageTest(TestCase):
    def test_about_page(self):
        response = Client().get('/about/')
        self.assertEqual(response.status_code, 200)
