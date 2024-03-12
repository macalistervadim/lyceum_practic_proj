import django.forms

import feedback.models


class FeedbackForm(django.forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = feedback.models.Feedback
        exclude = [
            feedback.models.Feedback.created_on.field.name,
            feedback.models.Feedback.status.field.name,
        ]

    def __str__(self):
        return f"обратная связь ({self.id})"


__all__ = []
