# Generated by Django 4.2.2 on 2023-11-28 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("game", "0010_remove_artist_answer_remove_artist_answer_slug_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="artist",
            name="name_slug",
            field=models.SlugField(
                default="", max_length=150, unique=True, verbose_name="Name Slug"
            ),
        ),
    ]
