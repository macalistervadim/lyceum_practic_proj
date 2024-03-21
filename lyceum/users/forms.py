import django.contrib.auth.forms
import django.contrib.auth.models
import django.forms as forms

import users.models as u_models


class SignUpForm(django.contrib.auth.forms.UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta(django.contrib.auth.forms.UserCreationForm.Meta):
        fields = [
            django.contrib.auth.models.User.email.field.name,
            django.contrib.auth.models.User.username.field.name,
            "password1",
            "password2",
        ]


class ProfileUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.birthday:
            self.initial["birthday"] = self.instance.birthday.strftime(
                "%Y-%m-%d",
            )

        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = u_models.Profile
        fields = [
            u_models.Profile.birthday.field.name,
            u_models.Profile.image.field.name,
        ]
        widgets = {
            u_models.Profile.birthday.field.name: forms.DateInput(
                attrs={"class": "form-control", "type": "date"},
            ),
            u_models.Profile.coffee_count.field.name: forms.NumberInput(
                attrs={
                    "readonly": "readonly",
                    "disabled": "disabled",
                },
            ),
        }


class UserChangeForm(django.contrib.auth.forms.UserChangeForm):
    password = None
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta(django.contrib.auth.forms.UserChangeForm.Meta):
        fields = [
            django.contrib.auth.models.User.first_name.field.name,
            django.contrib.auth.models.User.last_name.field.name,
            django.contrib.auth.models.User.email.field.name,
        ]
        exclude = [
            django.contrib.auth.models.User.password.field.name,
        ]


__all__ = []
