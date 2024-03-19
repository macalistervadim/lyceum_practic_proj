# Generated by Django 4.2 on 2024-03-19 14:00

from django.db import migrations
import sorl.thumbnail.fields
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_profile_options_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=sorl.thumbnail.fields.ImageField(
                blank=True,
                default=None,
                null=True,
                upload_to=users.models.item_directory_path,
                verbose_name='изображение',
            ),
        ),
    ]
