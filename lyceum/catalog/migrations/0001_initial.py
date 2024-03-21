# Generated by Django 4.2 on 2024-02-21 17:48

import catalog.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
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
                    "name",
                    models.CharField(
                        help_text="Введите название",
                        max_length=150,
                        unique=True,
                        verbose_name="название",
                    ),
                ),
                (
                    "is_published",
                    models.BooleanField(
                        default=True,
                        help_text="Дата публикации",
                        verbose_name="опубликовано",
                    ),
                ),
                (
                    "normalized_name",
                    models.CharField(
                        editable=False,
                        max_length=150,
                        unique=True,
                        verbose_name="исправленное значение",
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        help_text="Введите слаг для категории",
                        max_length=200,
                        verbose_name="слаг",
                    ),
                ),
                (
                    "weight",
                    models.IntegerField(
                        default=100,
                        help_text="Введите вес",
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(
                                32767
                            ),
                        ],
                        verbose_name="вес",
                    ),
                ),
            ],
            options={
                "verbose_name": "категория",
                "verbose_name_plural": "категории",
            },
        ),
        migrations.CreateModel(
            name="Tag",
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
                    "name",
                    models.CharField(
                        help_text="Введите название",
                        max_length=150,
                        unique=True,
                        verbose_name="название",
                    ),
                ),
                (
                    "is_published",
                    models.BooleanField(
                        default=True,
                        help_text="Дата публикации",
                        verbose_name="опубликовано",
                    ),
                ),
                (
                    "normalized_name",
                    models.CharField(
                        editable=False,
                        max_length=150,
                        unique=True,
                        verbose_name="исправленное значение",
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        help_text="Введите слаг для тэга",
                        max_length=200,
                        verbose_name="слаг",
                    ),
                ),
            ],
            options={
                "verbose_name": "тег",
                "verbose_name_plural": "теги",
            },
        ),
        migrations.CreateModel(
            name="Item",
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
                    "name",
                    models.CharField(
                        help_text="Введите название",
                        max_length=150,
                        unique=True,
                        verbose_name="название",
                    ),
                ),
                (
                    "is_published",
                    models.BooleanField(
                        default=True,
                        help_text="Дата публикации",
                        verbose_name="опубликовано",
                    ),
                ),
                (
                    "normalized_name",
                    models.CharField(
                        editable=False,
                        max_length=150,
                        unique=True,
                        verbose_name="исправленное значение",
                    ),
                ),
                (
                    "text",
                    models.TextField(
                        help_text="Введите сообщение",
                        validators=[
                            catalog.validators.ValidateMustContain(
                                "превосходно", "роскошно"
                            )
                        ],
                        verbose_name="текст",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        help_text="Выберите категорию",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="catalog.category",
                        verbose_name="категория",
                    ),
                ),
                (
                    "tags",
                    models.ManyToManyField(
                        help_text="Выберите тэг",
                        related_name="items",
                        to="catalog.tag",
                        verbose_name="теги",
                    ),
                ),
            ],
            options={
                "verbose_name": "товар",
                "verbose_name_plural": "товары",
            },
        ),
    ]
