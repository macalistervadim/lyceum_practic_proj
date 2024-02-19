from http import HTTPStatus

import django.core.validators
from django.test import Client, TestCase
from parameterized import parameterized

import catalog.models


class UrlTests(TestCase):

    @parameterized.expand(
        [
            ("/catalog", HTTPStatus.OK),
            ("/catalog/1", HTTPStatus.OK),
            ("/catalog/-1", HTTPStatus.NOT_FOUND),
            ("/catalog/string", HTTPStatus.NOT_FOUND),
        ],
    )
    def test_description(self, url, expected_status_code):
        self.check_response_status(url, expected_status_code)

    @parameterized.expand(
        [
            ("/catalog/re/124", HTTPStatus.OK),
            ("/catalog/re/124abs", HTTPStatus.NOT_FOUND),
            ("/catalog/re/-123", HTTPStatus.NOT_FOUND),
        ],
    )
    def test_catalog_regex(self, url, expected_status_code):
        self.check_response_status(url, expected_status_code)

    @parameterized.expand(
        [
            ("/catalog/converter/124", HTTPStatus.OK),
            ("/catalog/converter/124abs", HTTPStatus.NOT_FOUND),
            ("/catalog/converter/-123", HTTPStatus.NOT_FOUND),
        ],
    )
    def test_catalog_converter(self, url, expected_status_code):
        self.check_response_status(url, expected_status_code)

    def check_response_status(self, url, expected_status_code):
        response = Client().get(url, follow=True)
        self.assertEqual(
            response.status_code,
            expected_status_code,
            f"Status code != {expected_status_code}",
        )


class ModelTestCase(TestCase):
    def setUp(self):
        self.tag = catalog.models.Tag.objects.create(slug='test-tag', name='Test Tag')
        self.category = catalog.models.Category.objects.create(slug='test-category', name='Test Category')

    def test_valid_tag_slug(self):
        self.assertTrue(self.tag.pk)

    def test_valid_category_slug(self):
        self.assertTrue(self.category.pk)

    @parameterized.expand([
        ('valid-slug', 'Valid Category', 200),
        ('another-slug', 'Another Category', 300),
    ])
    def test_valid_category_weight(self, slug, name, weight):
        category = catalog.models.Category(slug=slug, name=name, weight=weight)
        category.full_clean()

    @parameterized.expand([
        ('invalid-slug', 'Invalid Category', -1),
        ('test-slug', 'Test Category', 400),
    ])
    def test_invalid_category_weight(self, slug, name, weight):
        category = catalog.models.Category(slug=slug, name=name, weight=weight)
        with self.assertRaises(django.core.exceptions.ValidationError):
            category.full_clean()

    @parameterized.expand([
        ("Этот товар превосходно подходит для ваших нужд", None),
        ("Роскошный тест для роскошного валидатора", None),
    ])
    def test_item_text_validator_positive(self, text, _):
        self.assertIsNone(catalog.models.validator_for_item_text(text))

    @parameterized.expand([
        ("Текст без ключевых слов", django.core.exceptions.ValidationError),
        ("Некорректный текст", django.core.exceptions.ValidationError),
    ])
    def test_item_text_validator_negative(self, text, expected_exception):
        with self.assertRaises(expected_exception):
            catalog.models.validator_for_item_text(text)
