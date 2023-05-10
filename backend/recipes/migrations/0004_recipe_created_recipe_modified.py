# Generated by Django 4.2 on 2023-05-09 19:48

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("recipes", "0003_rename_favourites_favorite_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="recipe",
            name="created",
            field=models.DateTimeField(
                auto_now_add=True,
                db_index=True,
                default=django.utils.timezone.now,
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="recipe",
            name="modified",
            field=models.DateTimeField(blank=True, db_index=True, null=True),
        ),
    ]
