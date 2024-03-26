# Generated by Django 4.2 on 2024-03-26 13:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("catalog", "0006_alter_item_is_on_main"),
    ]

    operations = [
        migrations.CreateModel(
            name="Rating",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "value",
                    models.IntegerField(
                        blank=True,
                        choices=[
                            (1, "ненависть"),
                            (2, "неприязнь"),
                            (3, "нейтрально"),
                            (4, "обожание"),
                            (5, "любовь"),
                        ],
                        null=True,
                        verbose_name="оценка",
                    ),
                ),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="catalog.item",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "рейтинг",
                "verbose_name_plural": "рейтинги",
                "ordering": ("user",),
            },
        ),
    ]
