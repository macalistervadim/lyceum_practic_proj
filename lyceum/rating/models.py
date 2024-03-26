import django.contrib.auth
import django.db
import django.utils.translation as translation

import catalog.models


class RatingChoices(django.db.models.TextChoices):
    HATE = translation.gettext_lazy("ненависть")
    DISLIKE = translation.gettext_lazy("неприязнь")
    NEUTRAL = translation.gettext_lazy("нейтрально")
    ADORE = translation.gettext_lazy("обожание")
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
    value = django.db.models.IntegerField(
        verbose_name=translation.gettext_lazy("оценка"),
        choices=(
            (1, RatingChoices.HATE),
            (2, RatingChoices.DISLIKE),
            (3, RatingChoices.NEUTRAL),
            (4, RatingChoices.ADORE),
            (5, RatingChoices.LOVE),
        ),
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ("user",)
        verbose_name = translation.gettext_lazy("рейтинг")
        verbose_name_plural = translation.gettext_lazy("рейтинги")


__all__ = []
