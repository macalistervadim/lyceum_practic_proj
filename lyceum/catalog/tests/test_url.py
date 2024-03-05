import django.core.validators
import django.test
import django.urls
import parameterized


class UrlTests(django.test.TestCase):
    @parameterized.parameterized.expand(
        [
            1,
            25,
            42,
            9999,
            0o123,
            "abc",
            0,
        ],
    )
    def test_item_list_reverse(self, pk):
        if isinstance(pk, int):
            url = django.urls.reverse("catalog:item_detail", kwargs={"pk": pk})
            self.assertEqual(url, f"/catalog/{pk}/")
        else:
            with self.assertRaises(django.urls.NoReverseMatch):
                django.urls.reverse("catalog:item_detail", kwargs={"pl": pk})

    @parameterized.parameterized.expand(
        [
            1,
            29,
            88,
            333,
            0o123,
            "abc",
            0,
        ],
    )
    def test_catalog_regex(self, pk):
        if isinstance(pk, int):
            url = django.urls.reverse(
                "catalog:catalog_regex",
                kwargs={"number": pk},
            )
            self.assertEqual(url, f"/catalog/re/{pk}/")
        else:
            with self.assertRaises(django.urls.NoReverseMatch):
                django.urls.reverse(
                    "catalog:catalog_regex",
                    kwargs={"number": pk},
                )

    @parameterized.parameterized.expand(
        [
            1,
            25,
            42,
            9239,
            0o123,
            "abc",
            0,
        ],
    )
    def test_catalog_converter(self, pk):
        if isinstance(pk, int):
            url = django.urls.reverse(
                "catalog:catalog_converter",
                kwargs={"number": pk},
            )
            self.assertEqual(url, f"/catalog/converter/{pk}/")
        else:
            with self.assertRaises(django.urls.NoReverseMatch):
                django.urls.reverse(
                    "catalog:catalog_converter",
                    kwargs={"number": pk},
                )

    def test_new_items_view(self):
        response = self.client.get(django.urls.reverse("catalog:new_items"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalog/item_filter_date.html")

    def test_friday_items_view(self):
        response = self.client.get(django.urls.reverse("catalog:friday_items"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalog/item_filter_date.html")

    def test_unverified_items_view(self):
        response = self.client.get(
            django.urls.reverse("catalog:unverified_items"),
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalog/item_filter_date.html")


__all__ = []
