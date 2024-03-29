# Generated by Django 5.0.1 on 2024-01-10 10:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("audio_lib", "0001_initial"),
        ("oauth", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="album",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="albums",
                to="oauth.authuser",
            ),
        ),
        migrations.AddField(
            model_name="comment",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comments",
                to="oauth.authuser",
            ),
        ),
        migrations.AddField(
            model_name="license",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="licenses",
                to="oauth.authuser",
            ),
        ),
        migrations.AddField(
            model_name="playlist",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="play_lists",
                to="oauth.authuser",
            ),
        ),
        migrations.AddField(
            model_name="track",
            name="album",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="audio_lib.album",
            ),
        ),
        migrations.AddField(
            model_name="track",
            name="genre",
            field=models.ManyToManyField(
                related_name="track_genres", to="audio_lib.genre"
            ),
        ),
        migrations.AddField(
            model_name="track",
            name="license",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="license_tracks",
                to="audio_lib.license",
            ),
        ),
        migrations.AddField(
            model_name="track",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tracks",
                to="oauth.authuser",
            ),
        ),
        migrations.AddField(
            model_name="track",
            name="user_of_likes",
            field=models.ManyToManyField(
                related_name="likes_of_tracks", to="oauth.authuser"
            ),
        ),
        migrations.AddField(
            model_name="playlist",
            name="tracks",
            field=models.ManyToManyField(
                related_name="track_play_lists", to="audio_lib.track"
            ),
        ),
        migrations.AddField(
            model_name="comment",
            name="track",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="track_comments",
                to="audio_lib.track",
            ),
        ),
    ]
