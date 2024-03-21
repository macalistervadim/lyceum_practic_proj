import http

import django.test
import django.urls

import users.models


class HomePageTest(django.test.TestCase):
    def test_home_page(self):
        url = django.urls.reverse("homepage:home")
        response = django.test.Client().get(url)
        self.assertEqual(
            response.status_code,
            http.HTTPStatus.OK,
            "Status code is not 200",
        )


class EndPointCoffeeTest(django.test.TestCase):
    def test_coffee_endpoint(self):
        user = django.contrib.auth.get_user_model().objects.create_user(
            username="testuser",
            password="testpassword",
        )
        users.models.Profile.objects.create(user=user)
        self.client.force_login(user)

        url = django.urls.reverse("homepage:coffee")
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            http.HTTPStatus.IM_A_TEAPOT,
            "Unexpected status code",
        )
        self.assertEqual(
            response.content.decode("utf-8"),
            "Я чайник",
            "Incorrect response text",
        )


__all__ = []
