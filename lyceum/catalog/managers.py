import django.db

import catalog.models


class ItemManager(django.db.models.Manager):
    def published(self):
        oredered_field_item_category = catalog.models.Item.category.field.name
        ordered_field_category_name = catalog.models.Category.name.field.name
        ordered_field_item_mainimage = (
            catalog.models.Item.main_image.related.name
        )
        ordered_field_mainimage = catalog.models.MainImage.image.field.name
        publish = self.get_queryset().filter(
            is_published=True,
            category__is_published=True,
        )
        order_by = publish.order_by(
            f"{oredered_field_item_category}__{ordered_field_category_name}",
            catalog.models.Item.name.field.name,
        )
        select_related = order_by.select_related(
            oredered_field_item_category,
            catalog.models.Item.main_image.related.name,
        )
        prefetch_related = select_related.prefetch_related(
            django.db.models.Prefetch(
                catalog.models.Item.tags.field.name,
                queryset=catalog.models.Tag.objects.filter(
                    is_published=True,
                ).only(
                    catalog.models.Tag.name.field.name,
                ),
            ),
        )
        return prefetch_related.only(
            catalog.models.Item.name.field.name,
            catalog.models.Item.text.field.name,
            f"{oredered_field_item_category}__"
            f"{ordered_field_category_name}",
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


__all__ = []
