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


__all__ = []
