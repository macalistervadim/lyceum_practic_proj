import django.test
import django.urls

import catalog.models


class HomePageContext(django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.published_category = catalog.models.Category.objects.create(
            name="Тестовая кат.",
        )
        cls.unpublished_category = catalog.models.Category.objects.create(
            name="Тестовая неопуб. кат.",
        )
        cls.published_tag = catalog.models.Tag.objects.create(
            name="Опубликованный тэг",
            slug="pub_tag",
            is_published=True,
        )
        cls.unpublished_tag = catalog.models.Tag.objects.create(
            name="Неопубликованный тэг",
            slug="unpub_tag",
            is_published=True,
        )
        cls.published_item = catalog.models.Item.objects.create(
            name="Опублик. товар",
            category=cls.published_category,
            text="превосходно",
            is_published=True,
            is_on_main=True,
        )
        cls.unpublished_item = catalog.models.Item.objects.create(
            name="Неопублик. товар",
            category=cls.unpublished_category,
            text="превосходно",
            is_published=False,
            is_on_main=False,
        )

        cls.published_item.tags.add(cls.published_tag.pk)
        cls.published_item.tags.add(cls.unpublished_tag.pk)

    def test_homepage_context(self):
        url = django.urls.reverse("homepage:home")
        response = self.client.get(url)
        self.assertIn("items", response.context)

        items = response.context["items"]
        for item in items:
            self.assertIsInstance(item, catalog.models.Item)

    def test_homepage_context_count(self):
        url = django.urls.reverse("homepage:home")
        response = self.client.get(url)
        items = response.context["items"]
        self.assertEqual(len(items), 1)


__all__ = []
