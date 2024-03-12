import django.contrib

import feedback.models


@django.contrib.admin.register(feedback.models.Feedback)
class AdminTag(django.contrib.admin.ModelAdmin):
    list_display = (
        feedback.models.Feedback.name.field.name,
        feedback.models.Feedback.status.field.name,
    )
    readonly_fields = (feedback.models.Feedback.created_on.field.name,)
    list_editable = (feedback.models.Feedback.status.field.name,)

    def save_model(self, request, obj, form, change):
        field = feedback.models.Feedback.status.field.name
        if field in form.changed_data:
            feedback.models.StatusLog(
                user=request.user,
                feedback=obj,
                _from=form.initial["status"],
                to=form.cleaned_data["status"],
            ).save()

        super().save_model(request, obj, form, change)


@django.contrib.admin.register(feedback.models.StatusLog)
class StatusLogAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        feedback.models.StatusLog.user.field.name,
        feedback.models.StatusLog.timestamp.field.name,
        feedback.models.StatusLog._from.field.name,
        feedback.models.StatusLog.to.field.name,
    )


__all__ = []
