# Generated by Django 4.2.2 on 2024-01-28 02:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="UserImage",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                ("image", models.ImageField(upload_to="raw/images/users/")),
                ("phash", models.CharField(default="", max_length=16)),
                ("average_hash", models.CharField(default="", max_length=16)),
                ("dhash", models.CharField(default="", max_length=16)),
                ("whash", models.CharField(default="", max_length=16)),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
