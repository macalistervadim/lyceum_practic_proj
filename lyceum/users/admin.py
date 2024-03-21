import django.contrib
import django.contrib.auth.admin
import django.contrib.auth.models

import users.models


class ProfileInline(django.contrib.admin.TabularInline):
    model = users.models.Profile
    can_delete = False


class UserAdmin(django.contrib.auth.admin.UserAdmin):
    inlines = (ProfileInline,)
    readonly_fields = [
        "profile_birthday",
        "profile_coffee_count",
        "profile_image",
    ]

    def profile_birthday(self, instance):
        return instance.profile.birthday

    profile_birthday.short_description = "Birthday"

    def profile_coffee_count(self, instance):
        return instance.profile.coffee_count

    profile_coffee_count.short_description = "Coffee Count"

    def profile_image(self, instance):
        return instance.profile.image

    profile_image.short_description = "Image"


django.contrib.admin.site.unregister(django.contrib.auth.models.User)
django.contrib.admin.site.register(
    django.contrib.auth.models.User,
    UserAdmin,
)


__all__ = []
