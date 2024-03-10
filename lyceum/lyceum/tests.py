import django.test
import django.urls


class RussianMiddlewareTest(django.test.TestCase):
    @django.test.override_settings(DJANGO_ALLOW_REVERSE=True)
    def test_reverse_enable_settings(self):
        url = django.urls.reverse("homepage:coffee")
        contents = {django.test.Client().get(url).content for _ in range(10)}
        self.assertIn("Я чайник".encode(), contents)
        self.assertIn("Я кинйач".encode(), contents)

    @django.test.override_settings(DJANGO_ALLOW_REVERSE=False)
    def test_reverse_disable_settings(self):
        url = django.urls.reverse("homepage:coffee")
        contents = {django.test.Client().get(url).content for _ in range(10)}
        self.assertIn("Я чайник".encode(), contents)
        self.assertNotIn("Я кинйач".encode(), contents)


__all__ = []
