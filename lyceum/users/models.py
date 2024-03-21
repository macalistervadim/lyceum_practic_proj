import pathlib
import uuid

import django.contrib.auth.models
import django.core.validators
import django.db
import django.utils.translation as translation
import sorl.thumbnail


class ProfileManager(django.db.models.Manager):
    def user_detail(self, pk):
        return (
            self.get_queryset()
            .filter(pk=pk)
            .values(
                "user__email",
                "user__first_name",
                "user__last_name",
                Profile.birthday.field.name,
                Profile.image.field.name,
                Profile.coffee_count.field.name,
            )
        )


def item_directory_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    profile_id_str = str(instance.id)
    return pathlib.Path("users") / profile_id_str / filename


class Profile(django.db.models.Model):
    objects = ProfileManager()

    user = django.db.models.OneToOneField(
        django.contrib.auth.models.User,
        on_delete=django.db.models.CASCADE,
    )
    birthday = django.db.models.DateField(
        translation.gettext_lazy("дата рождения"),
        null=True,
        blank=True,
        help_text=translation.gettext_lazy(
            "Выберите дату своего рождения",
        ),
    )
    coffee_count = django.db.models.PositiveIntegerField(
        translation.gettext_lazy("количество выпитого кофе"),
        null=False,
        default=0,
        help_text=translation.gettext_lazy("Счётчик выпитого кофе"),
    )
    image = django.db.models.ImageField(
        upload_to=item_directory_path,
        verbose_name=translation.gettext_lazy("изображение"),
        blank=True,
        null=True,
        help_text=translation.gettext_lazy("Аватарка"),
    )

    class Meta:
        verbose_name = translation.gettext_lazy("дополнительное поле")
        verbose_name_plural = translation.gettext_lazy(
            "дополнительные поля",
        )
        ordering = ("user",)

    def __str__(self):
        return self.user.username[:25]

    def get_image_350x350(self):
        return sorl.thumbnail.get_thumbnail(
            self.image,
            "350x350",
            crop="center",
            quality=85,
        )


__all__ = []
