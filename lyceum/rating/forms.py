import django.forms

import rating.models


class RatingForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = rating.models.Rating
        fields = [
            rating.models.Rating.value.field.name,
        ]


__all__ = []
