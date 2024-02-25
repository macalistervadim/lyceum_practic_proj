import itertools

import django.core.validators
import django.test
import django.urls
import parameterized

import catalog.models


class UrlTests(django.test.TestCase):
    @parameterized.parameterized.expand(
        [
            1,
            25,
            42,
            9999,
        ],
    )
    def test_item_list_reverse(self, pk):
        url = django.urls.reverse("catalog:item_detail", kwargs={"pk": pk})
        self.assertEqual(url, f"/catalog/{pk}/")

    @parameterized.parameterized.expand(
        [
            1,
            29,
            88,
            333,
        ],
    )
    def test_catalog_regex(self, pk):
        url = django.urls.reverse(
            "catalog:catalog_regex", kwargs={"number": pk},
        )
        self.assertEqual(url, f"/catalog/re/{pk}/")

    @parameterized.parameterized.expand(
        [
            1,
            25,
            42,
            9239,
        ],
    )
    def test_catalog_converter(self, pk):
        url = django.urls.reverse(
            "catalog:catalog_converter", kwargs={"number": pk},
        )
        self.assertEqual(url, f"/catalog/converter/{pk}/")


class DBItemTests(django.test.TestCase):
    category: catalog.models.Category
    tag: catalog.models.Tag

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.category = catalog.models.Category.objects.create(
            name="Test",
            slug="test-category-clug",
        )
        cls.tag = catalog.models.Tag.objects.create(
            name="Test",
            slug="test-slug-tag",
        )

    @parameterized.parameterized.expand(
        [
            ("test", "превосходно", True),
            ("test", "роскошно", True),
            ("test", "Я превосходно", True),
            ("test", "превосходно Я", True),
            ("test", "превосходно роскошно", True),
            ("test", "роскошно!", True),
            ("test", "!роскошно", True),
            ("test", "!роскошно", True),
            ("test", "роскошно©", True),
            ("test", "превосходноН", False),
            ("test", "превНосходно", False),
            ("test", "Нпревосходно", False),
            ("test", "Я превосх%одно", False),
            ("test", "превосходнороскошно", False),
            ("test" * 38, "превосходно", False),
        ],
    )
    def test_db_item(self, name, expected_text, expected_status_code):
        item_count = catalog.models.Item.objects.count()
        self.item = catalog.models.Item(
            name=name,
            text=expected_text,
            category=self.category,
        )
        if not expected_status_code:
            with self.assertRaises(django.core.validators.ValidationError):
                self.item.full_clean()
                self.item.tags.add(self.tag)
                self.item.save()
            self.assertEqual(
                catalog.models.Item.objects.count(),
                item_count,
                msg="Объект не добавлен",
            )
        else:
            self.item.full_clean()
            self.item.save()
            self.item.tags.add(self.tag)
            self.assertEqual(
                catalog.models.Item.objects.count(),
                item_count + 1,
                msg="Объект добавлен",
            )


class DBCategoryTests(django.test.TestCase):
    @parameterized.parameterized.expand(
        [
            ("test", "abs", 1, True),
            ("test", "1abs2", 1, True),
            ("test", "a12bs", 1, True),
            ("test", "ABS", 1, True),
            ("test", "-abs-", 1, True),
            ("test", "_abs_", 1, True),
            ("test", "_abs_", 32767, True),
            ("test", "Я", 1, False),
            ("test", "Яabs", 1, False),
            ("test", "Я abs", 1, False),
            ("test", "aЯbs", 1, False),
            ("test", "absЯ", 1, False),
            ("test", "abs Я", 1, False),
            ("test", "*abs*", 1, False),
            ("test", "a*bs", 1, False),
            ("test" * 38, "abs", 1, False),
            ("test", "abs" * 67, 1, False),
            ("test", "abs", 32768, False),
            ("test", "abs", 0, False),
            ("test", "abs", -1, False),
        ],
    )
    def test_db_category(self, name, slug, weight, expected_status_code):
        category_count = catalog.models.Category.objects.count()
        self.category = catalog.models.Category(
            name=name,
            slug=slug,
            weight=weight,
        )
        if not expected_status_code:
            with self.assertRaises(django.core.validators.ValidationError):
                self.category.full_clean()
                self.category.save()
            self.assertEqual(
                catalog.models.Item.objects.count(),
                category_count,
                msg="Объект не добавлен",
            )
        else:
            self.category.full_clean()
            self.category.save()
            self.assertEqual(
                catalog.models.Category.objects.count(),
                category_count + 1,
                msg="Объект добавлен",
            )


class DBItemTest(django.test.TestCase):
    @parameterized.parameterized.expand(
        [
            ("test", "abs", True),
            ("test", "1abs2", True),
            ("test", "a12bs", True),
            ("test", "ABS", True),
            ("test", "-abs-", True),
            ("test", "_abs_", True),
            ("test", "Я", False),
            ("test", "Яabs", False),
            ("test", "Я abs", False),
            ("test", "aЯbs", False),
            ("test", "absЯ", False),
            ("test", "abs Я", False),
            ("test", "*abs*", False),
            ("test", "a*bs", False),
            ("test" * 38, "abs", False),
            ("test", "abs" * 67, False),
        ],
    )
    def test_db_tag(self, name, slug, expected_status_code):
        tag_count = catalog.models.Tag.objects.count()
        self.tag = catalog.models.Tag(
            name=name,
            slug=slug,
        )
        if not expected_status_code:
            with self.assertRaises(django.core.validators.ValidationError):
                self.tag.full_clean()
                self.tag.save()
            self.assertEqual(
                catalog.models.Tag.objects.count(),
                tag_count,
                msg="Объект не добавлен",
            )
        else:
            self.tag.full_clean()
            self.tag.save()
            self.assertEqual(
                catalog.models.Tag.objects.count(),
                tag_count + 1,
                msg="Объект добавлен",
            )


class DBNormalizeTest(django.test.TestCase):
    @parameterized.parameterized.expand(
        (
            (x[0], x[1][0], x[1][1])
            for x in itertools.product(
                [
                    ("test"),
                    ("Тest"),
                    ("tЕst"),
                ],
                [
                    ("test test", True),
                    ("itfaketest", True),
                    ("test, test", True),
                    ("test!test", True),
                    ("testt", True),
                    ("test!", False),
                    ("!test", False),
                    ("!test!", False),
                    (" test ", False),
                    ("test,", False),
                    (".test", False),
                    ("te st", False),
                    ("te sТ", False),
                    ("tеst", False),
                ],
            )
        ),
    )
    def test_db_normalize_text(self, name1, name2, is_validate):
        tag_count = catalog.models.Category.objects.count()
        self.tag1 = catalog.models.Tag(
            name=name1,
            slug="1",
        )
        self.tag2 = catalog.models.Tag(
            name=name2,
            slug="2",
        )
        if not is_validate:
            with self.assertRaises(
                django.core.validators.ValidationError,
                msg=f"Добавлено {name2} а ожидалось {name1}",
            ):
                self.tag2.full_clean()
                self.tag2.save()
                self.tag1.full_clean()
                self.tag1.save()
            self.assertEqual(
                catalog.models.Tag.objects.count(),
                tag_count + 1,
                msg="Объекты не добавлены",
            )
        else:
            self.tag1.full_clean()
            self.tag1.save()
            self.tag2.full_clean()
            self.tag2.save()
            self.assertEqual(
                catalog.models.Tag.objects.count(),
                tag_count + 2,
                msg="Объекты добавлены",
            )


__all__ = []
