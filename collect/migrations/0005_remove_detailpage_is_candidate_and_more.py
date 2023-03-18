# Generated by Django 4.1.7 on 2023-03-13 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("collect", "0004_detailpage_is_candidate_detailpage_reviewed"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="detailpage",
            name="is_candidate",
        ),
        migrations.RemoveField(
            model_name="detailpage",
            name="reviewed",
        ),
        migrations.AddField(
            model_name="detailpage",
            name="approved",
            field=models.PositiveSmallIntegerField(
                choices=[(0, "Rejected"), (1, "Unset"), (2, "Approved")], default=1
            ),
        ),
    ]
