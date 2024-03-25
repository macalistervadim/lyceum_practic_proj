import django.contrib.auth
import django.db
import django.utils.translation as translation

import catalog.models


class RatingChoices(django.db.models.TextChoices):
    HATE = translation.gettext_lazy("ненависть")
    DISLIKE = translation.gettext_lazy("неприязнь")
    NEUTRAL = translation.gettext_lazy("нейтрально")
    ADORATION = translation.gettext_lazy("обожание")
    LOVE = translation.gettext_lazy("любовь")


class Rating(django.db.models.Model):
    user = django.db.models.ForeignKey(
        django.contrib.auth.get_user_model(),
        on_delete=django.db.models.CASCADE,
    )
    item = django.db.models.ForeignKey(
        catalog.models.Item,
        on_delete=django.db.models.CASCADE,
    )
    value = django.db.models.CharField(
        choices=RatingChoices.choices,
        max_length=11,
        verbose_name=translation.gettext_lazy("оценка"),
    )

    class Meta:
        ordering = ("user",)
        verbose_name = translation.gettext_lazy("рейтинг")
        verbose_name_plural = translation.gettext_lazy("рейтинги")

    def __str__(self):
        return self.value


__all__ = []
