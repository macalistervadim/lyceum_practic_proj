import http

import django.shortcuts
import django.test
import django.urls

import feedback.forms
import feedback.models


class ItemViewTest(django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form = feedback.forms.FeedbackForm()
        cls.form_data = {"mail": "invalid_email", "text": ""}
        cls.expected_errors = {
            "mail": ["Введите правильный адрес электронной почты."],
            "text": ["Обязательное поле."],
        }

    def test_form_in_context(self):
        response = self.client.get(
            django.shortcuts.reverse("feedback:feedback"),
        )
        form = response.context["form"]
        self.assertIsInstance(form, type(self.form))

    def test_form_fields(self):
        response = self.client.get(
            django.shortcuts.reverse("feedback:feedback"),
        )
        form = response.context["form"]
        self.assertEqual(form.fields["mail"].label, "Электронный адрес")
        self.assertEqual(form.fields["text"].label, "Текстовое поле")
        self.assertEqual(
            form.fields["mail"].help_text,
            "Адрес электронной почты",
        )
        self.assertEqual(
            form.fields["text"].help_text,
            "Введите текстовое поле обращения",
        )

    def test_form_submission_redirect(self):
        data = {"mail": "test@example.com", "text": "Тестовый текст"}
        response = self.client.post(
            django.shortcuts.reverse("feedback:feedback"),
            data,
        )
        redirected_response = self.client.get(response.url)
        self.assertEqual(response.status_code, http.HTTPStatus.FOUND)
        self.assertRedirects(
            response,
            django.shortcuts.reverse("feedback:feedback"),
        )
        self.assertIn("form", redirected_response.context)

    def test_form_errors(self):
        response = self.client.post(
            django.shortcuts.reverse("feedback:feedback"),
            self.form_data,
        )
        for field, errors in self.expected_errors.items():
            self.assertFormError(response, "form", field, errors)


__all__ = []
