# Generated by Django 5.0.1 on 2024-01-17 19:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("audio_lib", "0003_track_cover"),
    ]

    operations = [
        migrations.AlterField(
            model_name="playlist",
            name="tracks",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                related_name="track_play_lists",
                to="audio_lib.track",
            ),
        ),
    ]
