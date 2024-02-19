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
        self.tag = catalog.models.Tag.objects.create(
            slug="test-tag",
            name="Test Tag",
        )
        self.category = catalog.models.Category.objects.create(
            slug="test-category",
            name="Test Category",
        )

    def test_valid_tag_slug(self):
        self.assertTrue(self.tag.pk)

    def test_valid_category_slug(self):
        self.assertTrue(self.category.pk)

    @parameterized.expand(
        [
            ("invalid-slug", 500),
            ("valid-slug", -10),
            ("valid-slug", 100),
            ("valid-slug", 32767),
        ],
    )
    def test_category_weight_validation(self, slug, weight):
        try:
            catalog.models.Category.objects.create(slug=slug, weight=weight)
        except django.core.exceptions.ValidationError as e:
            if weight < 0:
                self.assertEqual(
                    e.message,
                    "Ensure this value is greater than or equal to 0.",
                )
            elif weight > 32767:
                self.assertEqual(
                    e.message,
                    "Ensure this value is less than or equal to 32767.",
                )
        else:
            category = catalog.models.Category.objects.get(
                slug=slug,
                weight=weight,
            )
            self.assertEqual(category.slug, slug)
            self.assertEqual(category.weight, weight)

    def test_valid_slug_validation(self):
        valid_slugs = [
            "valid-slug", "another-valid-slug", "yet-another-slug",
        ]
        for slug in valid_slugs:
            self.assertIsNone(catalog.models.validator_for_tag_slug(slug))

    def test_invalid_slug_validation(self):
        invalid_slugs = [
            "!@#", "invalid slug", "with space",
        ]
        for slug in invalid_slugs:
            with self.assertRaises(django.core.exceptions.ValidationError):
                catalog.models.validator_for_tag_slug(slug)

    @parameterized.expand(
        [
            ("превосходно", None),
            ("роскошно", None),
        ],
    )
    def test_item_text_validator_positive(self, text, _):
        self.assertIsNone(catalog.models.validator_for_item_text(text))

    @parameterized.expand(
        [
            (
                "Текст без ключевых слов",
                django.core.exceptions.ValidationError,
            ),
            ("некорректныйтекст", django.core.exceptions.ValidationError),
            ("роскошный!!!", django.core.exceptions.ValidationError),
            ("превосходный!!", django.core.exceptions.ValidationError),
            ("qwertyроскошный", django.core.exceptions.ValidationError),
        ],
    )
    def test_item_text_validator_negative(self, text, expected_exception):
        with self.assertRaises(expected_exception):
            catalog.models.validator_for_item_text(text)
