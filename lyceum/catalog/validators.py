import re

import django.core.exceptions
import django.utils.deconstruct


WORDS_REGEX = re.compile(r"\w+|\W+")


@django.utils.deconstruct.deconstructible
class ValidateMustContain:
    def __init__(self, *args):
        self.validate_words = {word.lower() for word in args}
        self.pattern = ", ".join(self.validate_words)

    def __call__(self, value):
        words = set(WORDS_REGEX.findall(value.lower()))
        print(words)
        if not self.validate_words & words:
            raise django.core.exceptions.ValidationError(
                f"В тексте '{value}' нет слов {self.pattern} ",
            )

val = ValidateMustContain("превосходно", "роскошно")
val("Это превосходно!")

def validator_for_item_text(value):
    words = set(WORDS_REGEX.findall(value.lower()))
    if not {"превосходно", "роскошно"} & words:
        raise django.core.exceptions.ValidationError(
            "Текст должен содержать слово 'превосходно' или 'роскошно'.",
        )


__all__ = []
