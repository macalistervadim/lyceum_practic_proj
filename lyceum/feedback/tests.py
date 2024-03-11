import http

import django.shortcuts
import django.test
import django.urls

import feedback.forms
import feedback.models


class ItemViewTest(django.test.TestCase):
    form_data: dict = {"mail": "invalid_email", "text": ""}
    data: dict = {"mail": "test@example.com", "text": "Тестовый текст"}
    expected_errors: dict = {
        "mail": ["Введите правильный адрес электронной почты."],
        "text": ["Обязательное поле."],
    }

    def setUp(self):
        self.form = feedback.forms.FeedbackForm()

    def test_form_is_in_context(self):
        response = self.client.get(
            django.shortcuts.reverse("feedback:feedback"),
        )
        form = response.context["form"]
        self.assertIsInstance(form, type(self.form))

    def test_form_fields_labels_and_help_text(self):
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
        initial_count = feedback.models.Feedback.objects.count()
        response = self.client.post(
            django.shortcuts.reverse("feedback:feedback"),
            self.data,
        )
        redirected_response = self.client.get(response.url)
        self.assertEqual(response.status_code, http.HTTPStatus.FOUND)
        self.assertRedirects(
            response,
            django.shortcuts.reverse("feedback:feedback"),
            status_code=http.HTTPStatus.FOUND,
            target_status_code=http.HTTPStatus.OK,
        )
        self.assertEqual(
            feedback.models.Feedback.objects.count(),
            initial_count + 1,
            "Объект не создан",
        )
        self.assertTrue(
            feedback.models.Feedback.objects.filter(**self.data).exists(),
            "Объект Feedback не был создан в базе данных.",
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
