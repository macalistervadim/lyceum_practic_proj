import django.conf
import django.contrib
import django.core.mail
import django.shortcuts
import django.utils.translation as translation
import django.views.generic

import feedback.forms


class FeedbackView(django.views.generic.FormView):
    template_name = "feedback/feedback.html"
    form_class = feedback.forms.FeedbackForm

    def form_valid(self, form):
        form.save()

        django.core.mail.send_mail(
            subject="Feedback",
            message=form.cleaned_data["text"],
            from_email=django.conf.settings.EMAIL_HOST,
            recipient_list=[form.cleaned_data["mail"]],
        )

        django.contrib.messages.success(
            self.request,
            translation.gettext_lazy(
                "Форма успешно отправлена.",
            ),
        )
        return django.shortcuts.redirect("feedback:feedback")


__all__ = []
