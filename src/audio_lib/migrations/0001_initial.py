# Generated by Django 5.0.1 on 2024-01-07 13:49

import django.core.validators
import django.db.models.deletion
import src.base.services
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('oauth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=1000)),
                ('private', models.BooleanField(default=False)),
                ('cover', models.ImageField(blank=True, null=True, upload_to=src.base.services.get_path_upload_cover_album, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg']), src.base.services.validate_size_image])),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='albums', to='oauth.authuser')),
            ],
        ),
        migrations.CreateModel(
            name='License',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=1000)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='licenses', to='oauth.authuser')),
            ],
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('link_of_author', models.CharField(blank=True, max_length=500, null=True)),
                ('file', models.FileField(upload_to=src.base.services.get_path_upload_track, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp3', 'wav'])])),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('plays_count', models.PositiveIntegerField(default=0)),
                ('download', models.PositiveIntegerField(default=0)),
                ('likes_count', models.PositiveIntegerField(default=0)),
                ('private', models.BooleanField(default=False)),
                ('album', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='audio_lib.album')),
                ('genre', models.ManyToManyField(related_name='track_genres', to='audio_lib.genre')),
                ('license', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='license_tracks', to='audio_lib.license')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tracks', to='oauth.authuser')),
                ('user_of_likes', models.ManyToManyField(related_name='likes_of_tracks', to='oauth.authuser')),
            ],
        ),
        migrations.CreateModel(
            name='PlayList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('cover', models.ImageField(blank=True, null=True, upload_to=src.base.services.get_path_upload_cover_playlist, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg']), src.base.services.validate_size_image])),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='play_lists', to='oauth.authuser')),
                ('tracks', models.ManyToManyField(related_name='track_play_lists', to='audio_lib.track')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=1000)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='oauth.authuser')),
                ('track', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='track_comments', to='audio_lib.track')),
            ],
        ),
    ]
