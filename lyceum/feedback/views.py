import django.conf
import django.contrib
import django.core.mail
import django.shortcuts

import feedback.forms


def feedback_view(request):
    template = "feedback/feedback.html"
    form = feedback.forms.FeedbackForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        mail = form.cleaned_data.get("mail")
        text = form.cleaned_data.get("text")

        feedback.models.Feedback.objects.create(
            mail=mail,
            text=text,
        )

        django.core.mail.send_mail(
            "mail form",
            text,
            django.conf.settings.EMAIL_HOST,
            [mail],
            fail_silently=False,
        )

        django.contrib.messages.success(request, "Форма успешно отправлена.")
        return django.shortcuts.redirect("feedback:feedback")

    context = {"form": form}
    return django.shortcuts.render(request, template, context)


__all__ = []
