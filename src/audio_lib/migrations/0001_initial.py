# Generated by Django 5.0.1 on 2024-01-10 10:05

import django.core.validators
import src.base.services
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=1000)),
                ('private', models.BooleanField(default=False)),
                ('cover', models.ImageField(blank=True, null=True, upload_to=src.base.services.get_path_upload_cover_album, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg']), src.base.services.validate_size_image])),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=1000)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='License',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='PlayList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('cover', models.ImageField(blank=True, null=True, upload_to=src.base.services.get_path_upload_cover_playlist, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg']), src.base.services.validate_size_image])),
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
            ],
        ),
    ]
