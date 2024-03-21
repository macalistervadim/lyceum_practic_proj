import datetime
import random

import django.db

import catalog.models


class ItemManager(django.db.models.Manager):
    def published(self):
        ordered_field_item_category = catalog.models.Item.category.field.name
        ordered_field_category_name = catalog.models.Category.name.field.name
        ordered_field_item_mainimage = "main_image"
        ordered_field_mainimage = catalog.models.MainImage.image.field.name

        queryset = (
            self.get_queryset()
            .filter(
                is_published=True,
                category__is_published=True,
            )
            .order_by(
                f"{ordered_field_item_category}"
                f"__{ordered_field_category_name}",
                catalog.models.Item.name.field.name,
            )
        )

        queryset = queryset.select_related(
            ordered_field_item_category,
            ordered_field_item_mainimage,
        )

        prefetch_tags = django.db.models.Prefetch(
            "tags",
            queryset=catalog.models.Tag.objects.filter(
                is_published=True,
            ).only(
                "name",
            ),
        )
        queryset = queryset.prefetch_related(prefetch_tags)

        return queryset.only(
            catalog.models.Item.name.field.name,
            catalog.models.Item.text.field.name,
            f"{ordered_field_item_category}__{ordered_field_category_name}",
            f"{ordered_field_item_mainimage}__{ordered_field_mainimage}",
        )

    def on_main(self):
        return (
            self.published()
            .filter(
                is_on_main=True,
            )
            .order_by(
                catalog.models.Item.name.field.name,
            )
        )

    def gallery_images(self):
        return self.published().prefetch_related(
            django.db.models.Prefetch("gallery_images"),
        )

    def unverified_items(self):
        time_interval = datetime.timedelta(seconds=1)
        filtered_field = catalog.models.Item.updated.field.name

        created__gte = {
            f"{filtered_field}__gte": django.db.models.F(filtered_field)
            - time_interval,
        }
        created__lte = {
            f"{filtered_field}__lte": django.db.models.F(filtered_field)
            + time_interval,
        }

        filter_item = self.on_main().filter(**created__gte, **created__lte)
        return filter_item.order_by("?")[:5]

    def friday_items(self):
        item = catalog.models.Item.objects.published()
        filter_item = item.filter(updated__week_day=6)
        filter_order = catalog.models.Item.updated.field.name
        return filter_item.order_by(f"-{filter_order}")

    def new_items(self):
        one_week_ago = django.utils.timezone.now() - datetime.timedelta(
            days=7,
        )

        new_items = catalog.models.Item.objects.published().filter(
            created__gte=one_week_ago,
        )
        return random.sample(
            list(new_items),
            min(len(new_items), 5),
        )


__all__ = []
