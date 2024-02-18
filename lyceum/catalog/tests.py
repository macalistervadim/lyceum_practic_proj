from http import HTTPStatus

from parameterized import parameterized

from django.test import Client, TestCase
import django.core.validators

import catalog.models


class UrlTests(TestCase):

    @parameterized.expand(
        [
            ("/catalog", HTTPStatus.OK),
            ("/catalog/1", HTTPStatus.OK),
            ("/catalog/-1", HTTPStatus.NOT_FOUND),
            ("/catalog/string", HTTPStatus.NOT_FOUND),
        ]
    )
    def test_description(self, url, expected_status_code):
        self.check_response_status(url, expected_status_code)

    @parameterized.expand(
        [
            ("/catalog/re/124", HTTPStatus.OK),
            ("/catalog/re/124abs", HTTPStatus.NOT_FOUND),
            ("/catalog/re/-123", HTTPStatus.NOT_FOUND),
        ]
    )
    def test_catalog_regex(self, url, expected_status_code):
        self.check_response_status(url, expected_status_code)

    @parameterized.expand(
        [
            ("/catalog/converter/124", HTTPStatus.OK),
            ("/catalog/converter/124abs", HTTPStatus.NOT_FOUND),
            ("/catalog/converter/-123", HTTPStatus.NOT_FOUND),
        ]
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

    fixtures = ["fixtures/data.json"]

    def test_valid_tag_slug(self):
        tag = catalog.models.Tag.objects.get(pk=1)
        self.assertTrue(tag.pk)

    def test_valid_category_slug(self):
        category = catalog.models.Category.objects.get(pk=1)
        self.assertTrue(category.pk)

    def test_valid_item_text(self):
        item = catalog.models.Item.objects.get(pk=1)
        self.assertTrue(item.pk)

    @parameterized.expand(
        [
            ("Этот товар превосходно подходит для ваших нужд", None),
            (
                "Этот товар хорош, но не превосходен",
                django.core.exceptions.ValidationError,
            ),
        ]
    )
    def test_validator_for_item_text(self, text, expected_exception):
        if expected_exception:
            with self.assertRaises(expected_exception):
                catalog.models.validator_for_item_text(text)
        else:
            self.assertIsNone(catalog.models.validator_for_item_text(text))

    @parameterized.expand(
        [
            ("tag-1234", None),
            ("tag$test", django.core.exceptions.ValidationError),
        ]
    )
    def test_validator_for_tag_slug(self, slug, expected_exception):
        if expected_exception:
            with self.assertRaises(expected_exception):
                catalog.models.validator_for_tag_slug(slug)
        else:
            self.assertIsNone(catalog.models.validator_for_tag_slug(slug))
