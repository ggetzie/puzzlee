# Generated by Django 4.2.2 on 2024-01-27 08:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("game", "0012_artworkimage_average_hash_artworkimage_dhash_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="artworkimage",
            name="average_hash",
        ),
        migrations.RemoveField(
            model_name="artworkimage",
            name="dhash",
        ),
        migrations.RemoveField(
            model_name="artworkimage",
            name="phash",
        ),
        migrations.RemoveField(
            model_name="artworkimage",
            name="whash",
        ),
    ]
