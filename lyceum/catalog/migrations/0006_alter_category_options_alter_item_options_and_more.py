# Generated by Django 4.2 on 2024-02-18 13:38

import catalog.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_alter_category_options_alter_item_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={
                'verbose_name': 'категория',
                'verbose_name_plural': 'категории',
            },
        ),
        migrations.AlterModelOptions(
            name='item',
            options={'verbose_name': 'товар', 'verbose_name_plural': 'товары'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'verbose_name': 'тэг', 'verbose_name_plural': 'тэги'},
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.CharField(
                help_text='Введите слаг для категории',
                max_length=200,
                unique=True,
                validators=[catalog.models.validator_for_tag_slug],
                verbose_name='слаг',
            ),
        ),
        migrations.AlterField(
            model_name='category',
            name='weight',
            field=models.IntegerField(
                default=100,
                help_text='Введите вес',
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(32767),
                ],
                verbose_name='вес',
            ),
        ),
        migrations.AlterField(
            model_name='item',
            name='text',
            field=models.TextField(
                help_text='Введите сообщение',
                validators=[catalog.models.validator_for_item_text],
                verbose_name='текст',
            ),
        ),
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.CharField(
                help_text='Введите слаг для тэга',
                max_length=200,
                unique=True,
                validators=[catalog.models.validator_for_tag_slug],
                verbose_name='слаг',
            ),
        ),
    ]
