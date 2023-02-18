# Generated by Django 4.1.7 on 2023-02-17 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("game", "0003_artist_added_by_artist_created_at_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="artist",
            name="answer",
            field=models.CharField(max_length=150, verbose_name="Answer"),
        ),
        migrations.AlterField(
            model_name="artwork",
            name="year",
            field=models.CharField(max_length=50),
        ),
    ]
