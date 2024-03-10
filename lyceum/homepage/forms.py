import django.forms


class EchoForm(django.forms.Form):
    text = django.forms.CharField(label="Текст", widget=django.forms.Textarea)


__all__ = []
