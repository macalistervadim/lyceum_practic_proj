import itertools

import django.core.validators
import django.test
import django.urls
import parameterized

import catalog.models


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
            ("test", "превосходно"),
            ("test", "роскошно"),
            ("test", "Я превосходно"),
            ("test", "превосходно Я"),
            ("test", "превосходно роскошно"),
            ("test", "!роскошно"),
            ("test", "!роскошно"),
            ("test", "роскошно©"),
        ],
    )
    def test_db_item(self, name, expected_text):
        item_count = catalog.models.Item.objects.count()
        self.item = catalog.models.Item(
            name=name,
            text=expected_text,
            category=self.category,
        )

        self.item.full_clean()
        self.item.save()
        self.item.tags.add(self.tag)
        self.assertEqual(
            catalog.models.Item.objects.count(),
            item_count + 1,
            msg="Объект добавлен",
        )

    @parameterized.parameterized.expand(
        [
            ("test", "превосходноН"),
            ("test", "превНосходно"),
            ("test", "Нпревосходно"),
            ("test", "Я превосх%одно"),
            ("test", "превосходнороскошно"),
            ("test" * 38, "превосходно"),
        ]
    )
    def test_db_item_invalid(self, name, expected_text):
        item_count = catalog.models.Item.objects.count()
        self.item = catalog.models.Item(
            name=name,
            text=expected_text,
            category=self.category,
        )
        with self.assertRaises(django.core.validators.ValidationError):
            self.item.full_clean()
            self.item.tags.add(self.tag)
            self.item.save()

        self.assertEqual(
            catalog.models.Item.objects.count(),
            item_count,
            msg="Объект не добавлен",
        )


class DBCategoryTests(django.test.TestCase):
    @parameterized.parameterized.expand(
        [
            ("test", "abs", 1),
            ("test", "1abs2", 1),
            ("test", "a12bs", 1),
            ("test", "ABS", 1),
            ("test", "-abs-", 1),
            ("test", "_abs_", 1),
            ("test", "_abs_", 32767),
        ],
    )
    def test_db_category(self, name, slug, weight):
        category_count = catalog.models.Category.objects.count()
        self.category = catalog.models.Category(
            name=name,
            slug=slug,
            weight=weight,
        )
        self.category.full_clean()
        self.category.save()
        self.assertEqual(
            catalog.models.Category.objects.count(),
            category_count + 1,
            msg="Объект добавлен",
        )

    @parameterized.parameterized.expand(
        [
            ("test", "Я", 1),
            ("test", "Яabs", 1),
            ("test", "Я abs", 1),
            ("test", "aЯbs", 1),
            ("test", "absЯ", 1),
            ("test", "abs Я", 1),
            ("test", "*abs*", 1),
            ("test", "a*bs", 1),
            ("test" * 38, "abs", 1),
            ("test", "abs" * 67, 1),
            ("test", "abs", 32768),
            ("test", "abs", 0),
            ("test", "abs", -1),
        ]
    )
    def test_db_category_invalid(self, name, slug, weight):
        category_count = catalog.models.Category.objects.count()
        self.category = catalog.models.Category(
            name=name,
            slug=slug,
            weight=weight,
        )
        with self.assertRaises(django.core.validators.ValidationError):
            self.category.full_clean()
            self.category.save()

        self.assertEqual(
            catalog.models.Item.objects.count(),
            category_count,
            msg="Объект не добавлен",
        )


class DBItemTest(django.test.TestCase):
    @parameterized.parameterized.expand(
        [
            ("test", "abs"),
            ("test", "1abs2"),
            ("test", "a12bs"),
            ("test", "ABS"),
            ("test", "-abs-"),
            ("test", "_abs_"),
        ],
    )
    def test_db_tag(self, name, slug):
        tag_count = catalog.models.Tag.objects.count()
        self.tag = catalog.models.Tag(
            name=name,
            slug=slug,
        )

        try:
            self.tag.full_clean()
            self.tag.save()
        except django.core.exceptions.ValidationError:
            pass

        self.assertEqual(
            catalog.models.Tag.objects.count(),
            tag_count + 1,
            msg="Объект добавлен",
        )

    @parameterized.parameterized.expand(
        [
            ("test", "Я"),
            ("test", "Яabs"),
            ("test", "Я abs"),
            ("test", "aЯbs"),
            ("test", "absЯ"),
            ("test", "abs Я"),
            ("test", "*abs*"),
            ("test", "a*bs"),
            ("test" * 38, "abs"),
            ("test", "abs" * 67),
        ],
    )
    def test_db_tag_invalid(self, name, slug):
        tag_count = catalog.models.Tag.objects.count()
        self.tag = catalog.models.Tag(
            name=name,
            slug=slug,
        )
        with self.assertRaises(django.core.validators.ValidationError):
            self.tag.full_clean()
            self.tag.save()

        self.assertEqual(
            catalog.models.Tag.objects.count(),
            tag_count,
            msg="Объект не добавлен",
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
                    ("test test"),
                    ("itfaketest"),
                    ("test, test"),
                    ("test!test"),
                    ("testt"),
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
        self.tag1.full_clean()
        self.tag1.save()
        self.tag2.full_clean()
        self.tag2.save()
        self.assertEqual(
            catalog.models.Tag.objects.count(),
            tag_count + 2,
            msg="Объекты добавлены",
        )

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
                    ("test!"),
                    ("!test"),
                    ("!test!"),
                    (" test "),
                    ("test,"),
                    (".test"),
                    ("te st"),
                    ("te s"),
                    ("test"),
                ],
            )
        ),
    )
    def test_db_normalize_text_invalid(self, name1, name2, is_validate):
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


class TestOtherNormalizedNames(django.test.TestCase):
    @parameterized.parameterized.expand(
        [
            ("Вот корги!", "bot-kop-Ги"),
            ("Вот корги!", "Вот корги!"),
            ("Вот корги!", "votkorgi"),
        ],
    )
    def test_name_normalization(self, name1, name2):

        category1 = catalog.models.Category.objects.create(name=name1)

        normalized_name = category1.normalized_name

        with self.assertRaises(django.db.utils.IntegrityError):
            catalog.models.Category.objects.create(
                name=name2,
                normalized_name=normalized_name,
            )


__all__ = []
