import django.forms


class EchoForm(django.forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    text = django.forms.CharField(label="Текст")


__all__ = []
