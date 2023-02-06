# Generated by Django 4.1 on 2023-02-06 10:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("explogger", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="buffer",
            name="addedby",
            field=models.ForeignKey(
                db_column="b_addedby",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="b_addedby",
                to=settings.AUTH_USER_MODEL,
                to_field="username",
            ),
        )
    ]
