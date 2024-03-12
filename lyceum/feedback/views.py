import django.conf
import django.contrib
import django.core.mail
import django.shortcuts

import feedback.forms


def feedback_view(request):
    template = "feedback/feedback.html"
    form = feedback.forms.FeedbackForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()

        django.core.mail.send_mail(
            subject="Feedback",
            message=form.cleaned_data["text"],
            from_email=django.conf.settings.EMAIL_HOST,
            recipient_list=[form.cleaned_data["mail"]],
        )

        django.contrib.messages.success(request, "Форма успешно отправлена.")
        return django.shortcuts.redirect("feedback:feedback")

    context = {"form": form}
    return django.shortcuts.render(request, template, context)


__all__ = []
