import django.contrib.auth.forms
import django.contrib.auth.models
import django.forms

import users.models


class UserChange(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = django.contrib.auth.models.User
        fields = ["email"]


class SignUpForm(django.contrib.auth.forms.UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta(UserChange.Meta):
        fields = [
            "email",
            "username",
            "password1",
            "password2",
        ]


class ProfileUpdateForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.birthday:
            self.initial["birthday"] = self.instance.birthday.strftime(
                "%Y-%m-%d",
            )

        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta(UserChange.Meta):
        model = users.models.Profile
        fields = [
            users.models.Profile.birthday.field.name,
            users.models.Profile.image.field.name,
        ]
        widgets = {
            users.models.Profile.birthday.field.name: django.forms.DateInput(
                attrs={"class": "form-control", "type": "date"},
            ),
            users.models.Profile.coffee_count.field.name:
                django.forms.NumberInput(
                attrs={
                    "readonly": "readonly",
                    "disabled": "disabled",
                },
            ),
        }


class UserChangeForm(UserChange):
    class Meta(UserChange.Meta):
        fields = ["first_name", "last_name"]


__all__ = []
