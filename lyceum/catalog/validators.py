import re

import django.core.exceptions
import django.utils.deconstruct
import django.utils.translation as translation


WORDS_REGEX = re.compile(r"\w+|\W+")


@django.utils.deconstruct.deconstructible
class ValidateMustContain:
    def __init__(self, *args):
        self.validate_words = {word.lower() for word in args}
        self.pattern = ", ".join(self.validate_words)

    def __call__(self, value):
        words = set(WORDS_REGEX.findall(value.lower()))
        if not self.validate_words & words:
            raise django.core.exceptions.ValidationError(
                translation.gettext_lazy(
                    f"В тексте '{value}' нет слов {self.pattern}"
                ),
            )


def validator_for_item_text(value):
    words = set(WORDS_REGEX.findall(value.lower()))
    if not {"превосходно", "роскошно"} & words:
        raise django.core.exceptions.ValidationError(
            translation.gettext_lazy(
                "Текст должен содержать слово 'превосходно' или 'роскошно'."
            ),
        )


__all__ = []
