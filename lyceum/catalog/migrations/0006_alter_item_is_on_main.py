# Generated by Django 4.2 on 2024-03-16 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "catalog",
            "0005_alter_category_options_alter_item_options_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="is_on_main",
            field=models.BooleanField(
                default=False, verbose_name="отображать для главной"
            ),
        ),
    ]
