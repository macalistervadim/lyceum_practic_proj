# Generated by Django 4.2 on 2024-02-19 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "catalog",
            "0001_initial_squashed_0007_alter_tag_options_alter_category_is_published_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="text",
            field=models.TextField(
                help_text="Введите сообщение", verbose_name="текст"
            ),
        ),
    ]
