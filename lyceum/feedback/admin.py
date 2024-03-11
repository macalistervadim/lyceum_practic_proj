import django.contrib

import feedback.models


@django.contrib.admin.register(feedback.models.Feedback)
class AdminTag(django.contrib.admin.ModelAdmin):
    readonly_fields = (feedback.models.Feedback.created_on.field.name,)


__all__ = []
