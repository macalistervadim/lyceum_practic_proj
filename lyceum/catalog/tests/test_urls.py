import http

import django.core.validators
import django.test
import django.urls
import parameterized

import catalog.models


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


class TestContentItems(django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.category_published = catalog.models.Category.objects.create(
            is_published=True,
            name="Тестовая опубликованная категория",
            slug="published-category",
        )
        cls.category_published.full_clean()
        cls.category_published.save()

        cls.tag_published = catalog.models.Tag.objects.create(
            is_published=True,
            name="Тестовый опубликованный тег",
            slug="published-tag",
        )
        cls.tag_published.full_clean()
        cls.tag_published.save()

        cls.item_published = catalog.models.Item.objects.create(
            is_published=True,
            name="Тестовый опубликованный предмет",
            text="превосходно",
            category=cls.category_published,
        )
        cls.item_published.full_clean()
        cls.item_published.save()

        cls.item_on_main = catalog.models.Item.objects.create(
            is_published=True,
            is_on_main=True,
            name="Тестовый предмет на главной странице",
            text="превосходно",
            category=cls.category_published,
        )
        cls.item_on_main.full_clean()
        cls.item_on_main.save()

        cls.item_unpublished = catalog.models.Item.objects.create(
            is_published=False,
            name="Тестовый неопубликованный предмет",
            text="превосходно",
            category=cls.category_published,
        )

        cls.item_unpublished.full_clean()
        cls.item_unpublished.save()

        cls.item_published.tags.add(cls.tag_published)
        cls.item_on_main.tags.add(cls.tag_published)
        cls.item_published.tags.add(cls.tag_published)

    def test_home_page_correct_context(self):
        response = self.client.get(django.urls.reverse("homepage:home"))
        self.assertIn("items", response.context)

    def test_item_list_page_correct_context(self):
        response = self.client.get(django.urls.reverse("catalog:item-list"))
        self.assertIn("items", response.context)

    def test_home_count_item(self):
        response = self.client.get(django.urls.reverse("homepage:home"))
        self.assertEqual(len(response.context["items"]), 1)

    def test_item_list_count_item(self):
        response = self.client.get(django.urls.reverse("catalog:item-list"))
        self.assertEqual(len(response.context["items"]), 2)

    def test_item_type(self):
        response = self.client.get(django.urls.reverse("catalog:item-list"))
        items = response.context["items"]
        self.assertIsInstance(items.first(), catalog.models.Item)

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

    @parameterized.parameterized.expand(
        (
            "is_published",
            "normalize_name",
            "created",
            "updated",
        ),
    )
    def test_filds_item_main(self, field_name):
        response = self.client.get(django.shortcuts.reverse("homepage:home"))
        self.assertNotIn(
            field_name,
            response.context["items"].first().__dict__,
            msg=f"find useless field '{field_name}' in main query",
        )

    @parameterized.parameterized.expand(
        (
            "is_published",
            "normalize_name",
            "created",
            "updated",
        ),
    )
    def test_filds_item_list(self, field_name):
        response = self.client.get(
            django.shortcuts.reverse("catalog:item-list"),
        )
        self.assertNotIn(
            field_name,
            response.context["items"].first().__dict__,
            msg=f"find useless field '{field_name}' in main query",
        )

    def test_filds_tags_main(self):
        correct_fields = [
            "_state",
            "id",
            "name",
            "_prefetch_related_val_item_id",
        ]
        response = self.client.get(django.shortcuts.reverse("homepage:home"))
        item = response.context["items"].first()
        tag = item._prefetched_objects_cache["tags"].first()
        self.assertQuerySetEqual(
            tag.__dict__,
            correct_fields,
            msg="not correct use field in main item.tags query",
        )


__all__ = []
