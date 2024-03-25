import django.contrib.auth.forms
import django.contrib.auth.views as auth_views
import django.urls

import users.views


app_name = "users"

urlpatterns = [
    django.urls.path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="users/login.html",
        ),
        name="login",
    ),
    django.urls.path(
        "logout/",
        auth_views.LogoutView.as_view(
            template_name="users/logout.html",
        ),
        name="logout",
    ),
    django.urls.path(
        "change-password/",
        auth_views.PasswordChangeView.as_view(
            template_name="users/password_change.html",
            success_url=django.urls.reverse_lazy(
                "users:change-password-done",
            ),
        ),
        name="change-password",
    ),
    django.urls.path(
        "change-password/done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="users/password_change_done.html",
        ),
        name="change-password-done",
    ),
    django.urls.path(
        "reset-password/",
        auth_views.PasswordResetView.as_view(
            template_name="users/password_reset.html",
            email_template_name="users/password_reset_email.html",
            subject_template_name="users/subjects/password_reset_subject.txt",
            success_url=django.urls.reverse_lazy(
                "users:password-reset-done",
            ),
        ),
        name="reset-password",
    ),
    django.urls.path(
        "reset-password/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="users/password_reset_done.html",
        ),
        name="password-reset-done",
    ),
    django.urls.path(
        "reset-password/confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html",
            success_url=django.urls.reverse_lazy(
                "users:password-reset-complete",
            ),
        ),
        name="password-reset-confirm",
    ),
    django.urls.path(
        "reset-password/complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html",
        ),
        name="password-reset-complete",
    ),
    django.urls.path(
        "signup/",
        users.views.RegistrationView.as_view(),
        name="signup",
    ),
    django.urls.path(
        "activate/<signed_username>/",
        users.views.ActivateView.as_view(),
        name="activate",
    ),
    django.urls.path(
        "user-list/",
        users.views.UserListView.as_view(),
        name="user-list",
    ),
    django.urls.path(
        "user-detail/<int:pk>/",
        users.views.UserDetailView.as_view(),
        name="user-detail",
    ),
    django.urls.path(
        "profile/",
        users.views.ProfileView.as_view(),
        name="profile",
    ),
]
