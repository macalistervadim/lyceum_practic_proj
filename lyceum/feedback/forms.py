import django.forms

import feedback.models


class FeedbackForm(django.forms.ModelForm):
    class Meta:
        model = feedback.models.Feedback
        exclude = [
            feedback.models.Feedback.created.field.name,
        ]


__all__ = []
