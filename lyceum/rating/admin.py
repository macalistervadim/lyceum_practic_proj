import django.contrib

import rating.models


@django.contrib.admin.register(rating.models.Rating)
class RatingAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        "user",
        "item",
        rating.models.Rating.value.field.name,
    )
    list_editable = (rating.models.Rating.value.field.name,)


__all__ = []
