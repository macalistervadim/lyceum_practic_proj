import django.test
import django.urls

import catalog.models


class ItemViewTest(django.test.TestCase):
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

        # cls.main_image = catalog.models.MainImage.objects.create(
        #     item=cls.published_item, image="main_image_items/enot_2reqxJv.jpg",
        # )

    def test_item_list_context(self):
        url = django.urls.reverse("catalog:item_list")
        response = self.client.get(url)
        items = response.context["items"]
        self.assertEqual(len(items), 1)
        for item in items:
            self.assertIsInstance(item, catalog.models.Item)

    def test_item_detail_context(self):
        url = django.urls.reverse(
            "catalog:item_detail",
            kwargs={"pk": self.published_item.pk},
        )
        response = self.client.get(url)
        self.assertIn("item", response.context)
        self.assertIn("main_image_url", response.context)
        self.assertIn("gallery_images_urls", response.context)

        item = response.context["item"]
        self.assertIsInstance(item, catalog.models.Item)
        self.assertEqual(item.name, "Опублик. товар")


__all__ = []
