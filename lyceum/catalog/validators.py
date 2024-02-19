import re

import django.core.exceptions
import django.utils.deconstruct


@django.utils.deconstruct.deconstructible
class ValidateMustContain:
    def __init__(self, *words):
        self.words = words
        self.pattern = "|".join(f"\\b{word}\\b" for word in words)

    def __call__(self, value):
        if re.findall(self.pattern, value, re.IGNORECASE):
            return
        str_words = " ".join(self.words)
        raise django.core.exceptions.ValidationError(
            f"Должно быть слово: {str_words}",
        )
