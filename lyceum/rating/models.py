import django.contrib.auth
import django.db
import django.utils.translation as translation

import catalog.models


class Rating(django.db.models.Model):
    class RatingChoices(django.db.models.IntegerChoices):
        HATE = 1, translation.gettext_lazy("Ненависть")
        DISLIKE = 2, translation.gettext_lazy("Неприязнь")
        NEUTRAL = 3, translation.gettext_lazy("Нейтрально")
        ADORE = 4, translation.gettext_lazy("Обожание")
        LOVE = 5, translation.gettext_lazy("Любовь")

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
        choices=RatingChoices.choices,
    )

    class Meta:
        ordering = ("user",)
        verbose_name = translation.gettext_lazy("рейтинг")
        verbose_name_plural = translation.gettext_lazy("рейтинги")


__all__ = []
