# Generated by Django 4.2 on 2024-03-12 11:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("feedback", "0002_feedback_name"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="feedback",
            options={
                "verbose_name": "обратная связь",
                "verbose_name_plural": "обратные связи",
            },
        ),
        migrations.AddField(
            model_name="feedback",
            name="status",
            field=models.CharField(
                choices=[
                    ("получено", "New"),
                    ("в обработке", "Pending"),
                    ("ответ дан", "Complete"),
                ],
                default="получено",
                max_length=11,
                verbose_name="статус обработки",
            ),
        ),
        migrations.AlterField(
            model_name="feedback",
            name="name",
            field=models.CharField(
                blank=True,
                help_text="Необязательное поле. Укажите имя отправителя. Максимальная длинна - 256 символов.",
                max_length=150,
                null=True,
                verbose_name="имя отправителя",
            ),
        ),
        migrations.CreateModel(
            name="StatusLog",
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
                    "timestamp",
                    models.DateTimeField(
                        auto_now_add=True,
                        help_text="дата и время изменения",
                        null=True,
                        verbose_name="дата и время изменения",
                    ),
                ),
                (
                    "_from",
                    models.CharField(
                        choices=[
                            ("получено", "New"),
                            ("в обработке", "Pending"),
                            ("ответ дан", "Complete"),
                        ],
                        db_column="from",
                        max_length=11,
                        verbose_name="перешло из состояния",
                    ),
                ),
                (
                    "to",
                    models.CharField(
                        choices=[
                            ("получено", "New"),
                            ("в обработке", "Pending"),
                            ("ответ дан", "Complete"),
                        ],
                        max_length=11,
                        verbose_name="перешло в состояние",
                    ),
                ),
                (
                    "feedback",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="feedback.feedback",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "журнал состояния",
                "verbose_name_plural": "журнал состояний",
            },
        ),
    ]
