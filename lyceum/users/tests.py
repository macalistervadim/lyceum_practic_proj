import unittest.mock

import django.contrib.auth.models as auth_models
import django.core
import django.test
import django.urls
from django.utils import timezone


from lyceum import settings
import users.models


class RegistrationTestCase(django.test.TestCase):
    def setUp(self):
        self.url = django.urls.reverse("users:signup")
        self.valid_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "TestPassword123",
            "password2": "TestPassword123",
        }

    @unittest.mock.patch("users.views.django.core.mail.send_mail")
    def test_registration_success(self, mock_send_mail):
        response = self.client.post(self.url, data=self.valid_data)
        self.assertRedirects(response, django.urls.reverse("users:login"))
        self.assertTrue(
            django.contrib.auth.models.User.objects.filter(
                username=self.valid_data["username"],
            ),
        )
        mock_send_mail.assert_called_once_with(
            subject="Активация профиля",
            message=unittest.mock.ANY,
            from_email=unittest.mock.ANY,
            recipient_list=["test@example.com"],
        )

    def test_registration_invalid_data(self):
        invalid_data = self.valid_data.copy()
        invalid_data["password2"] = "DifferentPassword"
        response = self.client.post(self.url, data=invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response,
            "form",
            "password2",
            "Введенные пароли не совпадают.",
        )


class ActivateTestCase(django.test.TestCase):
    def test_activate_success(self):

        user = auth_models.User.objects.create(
            username="testuser",
            email="test@example.com",
            is_active=False,
        )

        signer = django.core.signing.TimestampSigner()
        signed_username = signer.sign(user.username)
        response = self.client.get(
            django.urls.reverse(
                "users:activate",
                kwargs={"signed_username": signed_username},
            ),
        )
        self.assertTemplateUsed(response, "users/activation_success.html")
        user.refresh_from_db()
        self.assertTrue(user.is_active)

    def test_activate_invalid_signature(self):
        response = self.client.get(
            django.urls.reverse(
                "users:activate",
                kwargs={"signed_username": "invalid_signature"},
            ),
        )
        self.assertEqual(response.status_code, 404)

    def test_activate_expired_signature(self):
        user = auth_models.User.objects.create(
            username="testuser",
            email="test@example.com",
            is_active=False,
        )
        signer = django.core.signing.TimestampSigner()
        signed_username = signer.sign(user.username)
        expired_signed_username = signed_username + ":invalid_signature"
        response = self.client.get(
            django.urls.reverse(
                "users:activate",
                kwargs={"signed_username": expired_signed_username},
            ),
        )
        self.assertEqual(response.status_code, 404)


class BirthdayContextProcessorTest(django.test.TestCase):
    def setUp(self):

        self.client = django.test.Client()

        user_birthday = auth_models.User.objects.create_user(
            username="testuser",
            password="qwdfvbhjio",
        )
        self.profile_birthday = users.models.Profile.objects.create(
            user=user_birthday, birthday=timezone.now().date()
        )

        user_no_birthday = auth_models.User.objects.create_user(
            username="testuser_no_birtday",
            password="qwdfvbhjio1",
        )

        self.profile_no_birthday = users.models.Profile.objects.create(
            user=user_no_birthday,
            birthday="2001-10-10",
        )

    @unittest.mock.patch("users.context_processors.get_timezone_from_ip")
    def test_birthday_context_processor(self, mock_get_timezone_from_ip):
        mock_get_timezone_from_ip.return_value = settings.TIME_ZONE

        self.client.login(username="testuser", password="qwdfvbhjio")

        response = self.client.get("/")

        self.assertIn(
            self.profile_birthday,
            response.context["profiles_with_birthday_today"],
        )
        self.assertNotIn(
            self.profile_no_birthday,
            response.context["profiles_with_birthday_today"],
        )

        response = self.client.get("/catalog/")

        self.assertIn(
            self.profile_birthday,
            response.context["profiles_with_birthday_today"],
        )
        self.assertNotIn(
            self.profile_no_birthday,
            response.context["profiles_with_birthday_today"],
        )


__all__ = []
