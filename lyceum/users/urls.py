import django.contrib.auth.views
import django.contrib.auth.forms
import django.urls

import users.views

app_name = "users"

urlpatterns = [
    django.urls.path(
        "login/",
        django.contrib.auth.views.LoginView.as_view(
            template_name="users/login.html",
        ),
        name="login",
    ),
    django.urls.path(
        "logout/",
        django.contrib.auth.views.LogoutView.as_view(),
        name="logout",
    ),
    django.urls.path(
        "change-password/",
        django.contrib.auth.views.PasswordChangeView.as_view(
            template_name="users/change_password.html",
            success_url=django.urls.reverse_lazy('users:change-password-done'),
        ),
        name="change-password",
    ),
    django.urls.path(
        "change-password/done/",
        django.contrib.auth.views.PasswordChangeDoneView.as_view(
            template_name="users/change_password_done.html",
        ),
        name="change-password-done",
    ),
    django.urls.path(
        "reset-password/",
        django.contrib.auth.views.PasswordResetView.as_view(
            template_name="users/reset_password.html",
            email_template_name='users/password_reset_email.html',
            subject_template_name='users/subjects/password_reset_subject.txt',
            success_url = django.urls.reverse_lazy("users:password-reset-done")
        ),
        name="reset-password",
    ),
    django.urls.path(
        "reset-password/done/",
        django.contrib.auth.views.PasswordResetDoneView.as_view(
            template_name="users/reset_password_done.html",
        ),
        name="password-reset-done",
    ),
    django.urls.path(
        "reset-password/confirm/<uidb64>/<token>/",
        django.contrib.auth.views.PasswordResetConfirmView.as_view(
            template_name="users/reset_password_confirm.html",
            success_url=django.urls.reverse_lazy("users:password-reset-complete")
        ),
        name="password-reset-confirm",
    ),
    django.urls.path(
        "reset-password/complete/",
        django.contrib.auth.views.PasswordResetCompleteView.as_view(
            template_name="users/reset_password_complete.html",
        ),
        name="password-reset-complete",
    ),
    django.urls.path(
        "signup/",
        users.views.registration, name="signup",
    ),
    django.urls.path(
        "activate/<signed_username>/",
        users.views.activate, name="activate",
    ),
    django.urls.path(
        "user-list/",
        users.views.user_list, name="user-list",
    ),
    django.urls.path(
        "user-detail/<int:pk>/",
        users.views.user_detail, name="user-detail",
    ),
]
