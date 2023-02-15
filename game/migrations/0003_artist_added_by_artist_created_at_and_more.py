# Generated by Django 4.1.6 on 2023-02-13 13:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("game", "0002_artwork_added_by_artwork_created_at_artwork_year_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="artist",
            name="added_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="artist",
            name="created_at",
            field=models.DateTimeField(
                default=django.utils.timezone.now, verbose_name="Created at"
            ),
        ),
        migrations.AlterField(
            model_name="artwork",
            name="created_at",
            field=models.DateTimeField(
                default=django.utils.timezone.now, verbose_name="Created at"
            ),
        ),
    ]