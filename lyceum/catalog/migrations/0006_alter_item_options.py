# Generated by Django 4.2 on 2024-03-03 10:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_item_is_on_main_alter_galleryimage_image_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={
                'ordering': ('name',),
                'verbose_name': 'товар',
                'verbose_name_plural': 'товары',
            },
        ),
    ]