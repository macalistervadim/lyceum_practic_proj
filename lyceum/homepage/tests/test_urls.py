import http

import django.contrib.auth.models as auth_models
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
        user = auth_models.User.objects.create(
            username="testuser",
        )
        users.models.Profile.objects.create(user=user)

        self.client.force_login(user)

        url = django.urls.reverse("homepage:coffee")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 418)

        updated_profile = users.models.Profile.objects.get(user=user)
        self.assertEqual(updated_profile.coffee_count, 1)


__all__ = []
