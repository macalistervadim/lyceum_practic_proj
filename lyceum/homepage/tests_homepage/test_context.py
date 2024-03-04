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

    def test_on_main_queryset_fields(self):
        item_model = catalog.models.Item

        all_fields = {field.name for field in item_model._meta.get_fields()}

        internal_fields = {"_state", "_prefetched_objects_cache"}
        additional_fields = {"gallery_image", "tags", "mainimage"}

        expected_fields = all_fields - internal_fields - additional_fields
        items_on_main = item_model.objects.on_main()

        for item in items_on_main:
            item_fields = {field.name for field in item._meta.fields}
            self.assertEqual(item_fields, expected_fields)

    def test_not_existing_fields_in_db_answer(self):
        item_model = catalog.models.Item

        additional_fields = {'gallery_image', 'tags', 'mainimage'}

        items_on_main = item_model.objects.on_main()

        for item in items_on_main:
            for field in additional_fields:
                self.assertNotIn(field, item.__dict__,
                                f"{field} field should not exist in the DB answer")

    def test_prefetched_objects_in_db_answer(self):
        item = catalog.models.Item.objects.on_main().first()
        
        self.assertNotIn('tags', item._prefetched_objects_cache,
                        "Prefetched objects should not exist in the DB answer")


__all__ = []
