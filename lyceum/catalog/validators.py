import django.core.validators
from django.utils.translation import gettext_lazy as _


class ValidateMustContain:
    def __init__(self, *words):
        self.words = words

    def __call__(self, value):
        missing_words = [word for word in self.words if word.lower()
                         not in value.lower()]
        if missing_words:
            raise django.core.exceptions.ValidationError(
                _("Следующие слова должны присутствовать"
                  " в тексте: %(words)s."),
                params={"words": ", ".join(missing_words)},
            )
        return value
