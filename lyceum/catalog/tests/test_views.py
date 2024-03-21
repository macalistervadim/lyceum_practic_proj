import django.test
import django.urls

import catalog.models


class ItemViewTest(django.test.TestCase):
    ignored_fields = ["is_published", "gallery_image"]

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

    def test_item_list_context(self):
        url = django.urls.reverse("catalog:item-list")
        response = self.client.get(url)
        items = response.context["items"]
        self.assertEqual(len(items), 1)
        for item in items:
            self.assertIsInstance(
                item,
                catalog.models.Item,
                msg="Expected 'Item' instance in 'items' context",
            )

    def test_item_detail_context(self):
        url = django.urls.reverse(
            "catalog:item-detail",
            kwargs={"pk": self.published_item.pk},
        )
        response = self.client.get(url)
        self.assertIn(
            "item",
            response.context,
            msg="Expected 'item' in response context",
        )

        item = response.context["item"]
        self.assertIsInstance(
            item,
            catalog.models.Item,
            msg="Expected 'Item' instance in 'item' context",
        )
        self.assertEqual(
            item.name,
            "Опублик. товар",
            msg="Unexpected item name in context",
        )

    def test_fields_item_published(self):
        response = self.client.get(
            django.urls.reverse("catalog:item-list"),
        )
        for field_name in self.ignored_fields:
            self.assertNotIn(
                field_name,
                response.context["items"].first().__dict__,
                msg=f"Field '{field_name}' found in Item instance, "
                "but should be ignored",
            )

    def test_fields_tags_published(self):
        response = self.client.get(
            django.urls.reverse("catalog:item-list"),
        )
        items = response.context["items"]
        for item in items:
            if hasattr(item, "tag_names"):
                tag_names = getattr(item, "tag_names", [])
                for tag in tag_names:
                    expected_fields = ["_state", "id", "name"]
                    if hasattr(tag, "_prefetch_related_val_item_id"):
                        expected_fields.append(
                            "_prefetch_related_val_item_id",
                        )

                    self.assertNotIn(
                        "_prefetched_objects_cache",
                        tag.__dict__,
                        msg="Unexpected '_prefetched_objects_cache' "
                        "attribute in Tag instance",
                    )

                    self.assertQuerySetEqual(
                        tag.__dict__,
                        expected_fields,
                        msg="Unexpected fields in Tag instance",
                    )


__all__ = []
