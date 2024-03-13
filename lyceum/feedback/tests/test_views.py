import http

import django.core.files.uploadedfile
import django.shortcuts
import django.test
import django.urls

import feedback.forms
import feedback.models


class ItemViewTest(django.test.TestCase):
    form_data = {"mail": "invalid_email", "text": ""}
    expected_errors = {
        "mail": ["Введите правильный адрес электронной почты."],
        "text": ["Обязательное поле."],
    }
    data = {
        "text": "some test text",
        "mail": "test@test.com",
        "name": "Rick",
    }

    def test_form_errors(self):
        response = self.client.post(
            django.shortcuts.reverse("feedback:feedback"),
            self.form_data,
        )
        for field, errors in self.expected_errors.items():
            self.assertFormError(
                response, "form", field, errors, "Not found expected errors"
            )

    def test_form_in_context(self):
        response = self.client.get(
            django.shortcuts.reverse("feedback:feedback"),
        )
        self.assertIn("form", response.context, "Respone not found form")

    def test_form_labels(self):
        response = self.client.get(
            django.shortcuts.reverse("feedback:feedback"),
        )
        form = response.context["form"]
        self.assertEqual(
            form.fields["mail"].label,
            "Электронный адрес",
            "Form not found field Электронный адрес",
        )
        self.assertEqual(
            form.fields["text"].label,
            "Текстовое поле",
            "Form not found field Текстовое поле",
        )

    def test_form_help_texts(self):
        response = self.client.get(
            django.shortcuts.reverse("feedback:feedback"),
        )
        form = response.context["form"]
        self.assertEqual(
            form.fields["mail"].help_text,
            "Адрес электронной почты",
            "Form not found help_text Адрес электронной почты",
        )
        self.assertEqual(
            form.fields["text"].help_text,
            "Введите текстовое поле обращения",
            "Form not found help_text Введите текстовое поле обращения",
        )

    def test_request_method_get(self):
        response = self.client.get(
            django.shortcuts.reverse("feedback:feedback"),
        )
        self.assertEqual(
            response.status_code,
            http.HTTPStatus.OK,
            f"status code != {http.HTTPStatus.OK}",
        )

    def test_request_method_post(self):
        response = self.client.post(
            django.shortcuts.reverse("feedback:feedback"),
            self.data,
            follow=True,
        )
        self.assertEqual(
            response.status_code,
            http.HTTPStatus.OK,
            f"status code != {http.HTTPStatus.OK}",
        )

    def test_submit_redirect(self):
        item_count = feedback.models.Feedback.objects.count()
        response = self.client.post(
            django.shortcuts.reverse("feedback:feedback"),
            self.data,
            follow=True,
        )
        self.assertRedirects(
            response,
            django.shortcuts.reverse("feedback:feedback"),
            status_code=http.HTTPStatus.FOUND,
            target_status_code=http.HTTPStatus.OK,
        )
        self.assertIn("form", response.context, "Respone not found form")
        form = response.context["form"]
        self.assertEqual(
            form.fields["mail"].label,
            "Электронный адрес",
            "Form dont have field Электронный адрес",
        )
        self.assertEqual(
            form.fields["text"].label,
            "Текстовое поле",
            "Form dont have field Текстовое поле",
        )
        self.assertEqual(
            feedback.models.Feedback.objects.count(),
            item_count + 1,
            "Objects dont created",
        )
        self.assertTrue(
            feedback.models.Feedback.objects.filter(
                mail="test@test.com",
            ).exists(),
            "Object dont created",
        )


__all__ = []
