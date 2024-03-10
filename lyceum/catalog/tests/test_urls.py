import http

import django.core.validators
import django.test
import django.urls
import parameterized


class UrlTests(django.test.TestCase):
    PARAMETRIZED_PARAMETERS = [
        1,
        25,
        42,
        9999,
        0o123,
        "abc",
        0,
        -0,
        0o10,
        "01",
        "010",
        -123,
        0.231,
        1.1231,
        "123adfs",
        "asdad1123",
        "10^2",
        "123$abc",
        "abc%123",
    ]

    @parameterized.parameterized.expand(PARAMETRIZED_PARAMETERS)
    def test_item_list_reverse(self, pk):
        try:
            if isinstance(pk, int):
                url = django.urls.reverse(
                    "catalog:item-detail",
                    kwargs={"pk": pk},
                )
                response = self.client.get(url)
                if response.status_code == http.HTTPStatus.OK:
                    self.assertEqual(
                        response.status_code,
                        http.HTTPStatus.OK,
                        f"Unexpected status code: {response.status_code}",
                    )
                elif response.status_code == http.HTTPStatus.NOT_FOUND:
                    self.assertEqual(
                        response.status_code,
                        http.HTTPStatus.NOT_FOUND,
                        f"Unexpected status code: {response.status_code}",
                    )
                else:
                    self.fail(
                        f"Unexpected status code: {response.status_code}",
                    )
        except django.urls.exceptions.NoReverseMatch:
            pass

    @parameterized.parameterized.expand(PARAMETRIZED_PARAMETERS)
    def test_catalog_regex(self, pk):
        try:
            if isinstance(pk, int):
                url = django.urls.reverse(
                    "catalog:catalog-regex",
                    kwargs={"pk": pk},
                )
                response = self.client.get(url)
                if response.status_code == http.HTTPStatus.OK:
                    self.assertEqual(
                        response.status_code,
                        http.HTTPStatus.OK,
                        f"Unexpected status code: {response.status_code}",
                    )
                elif response.status_code == http.HTTPStatus.NOT_FOUND:
                    self.assertEqual(
                        response.status_code,
                        http.HTTPStatus.NOT_FOUND,
                        f"Unexpected status code: {response.status_code}",
                    )
                else:
                    self.fail(
                        f"Unexpected status code: {response.status_code}",
                    )
        except django.urls.exceptions.NoReverseMatch:
            pass

    @parameterized.parameterized.expand(PARAMETRIZED_PARAMETERS)
    def test_catalog_converter(self, pk):
        try:
            if isinstance(pk, int):
                url = django.urls.reverse(
                    "catalog:catalog-converter",
                    kwargs={"pk": pk},
                )
                response = self.client.get(url)
                if response.status_code == http.HTTPStatus.OK:
                    self.assertEqual(
                        response.status_code,
                        http.HTTPStatus.OK,
                        f"Unexpected status code: {response.status_code}",
                    )
                elif response.status_code == http.HTTPStatus.NOT_FOUND:
                    self.assertEqual(
                        response.status_code,
                        http.HTTPStatus.NOT_FOUND,
                        f"Unexpected status code: {response.status_code}",
                    )
                else:
                    self.fail(
                        f"Unexpected status code: {response.status_code}",
                    )
        except django.urls.exceptions.NoReverseMatch:
            pass

    def test_new_items_view(self):
        response = self.client.get(django.urls.reverse("catalog:new-items"))
        self.assertEqual(
            response.status_code,
            http.HTTPStatus.OK,
            "Expected status code: 200, Actual status code:  "
            f"{response.status_code}",
        )
        self.assertTemplateUsed(
            response,
            "catalog/item_filter_date.html",
            "The current template differs from the one specified "
            "in the view function",
        )

    def test_friday_items_view(self):
        response = self.client.get(django.urls.reverse("catalog:friday-items"))
        self.assertEqual(
            response.status_code,
            http.HTTPStatus.OK,
            "Expected status code: 200, Actual status code: "
            f"{response.status_code}",
        )
        self.assertTemplateUsed(
            response,
            "catalog/item_filter_date.html",
            "The current template differs from the one specified "
            "in the view function",
        )

    def test_unverified_items_view(self):
        response = self.client.get(
            django.urls.reverse("catalog:unverified-items"),
        )
        self.assertEqual(
            response.status_code,
            http.HTTPStatus.OK,
            "Expected status code: 200, Actual status code: "
            f"{response.status_code}",
        )
        self.assertTemplateUsed(
            response,
            "catalog/item_filter_date.html",
            "The current template differs from the "
            " one specified in the view function ",
        )


__all__ = []
