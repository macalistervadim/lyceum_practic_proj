import django.contrib.auth.forms
import django.contrib.auth.models
import django.forms

import users.models


class SignUpForm(django.contrib.auth.forms.UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = django.contrib.auth.models.User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )


class ProfileUpdateForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.birthday:
            self.initial["birthday"] = self.instance.birthday.strftime(
                "%Y-%m-%d"
            )

        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = users.models.Profile
        fields = ["birthday", "image"]
        widgets = {
            "birthday": django.forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            )
        }


class UserUpdateForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = django.contrib.auth.models.User
        fields = ["email", "first_name", "last_name"]


__all__ = []
