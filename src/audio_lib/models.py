from django.core.validators import FileExtensionValidator
from django.db import models

from src.base.services import validate_size_image, get_path_upload_cover_album
from src.oauth.models import AuthUser


class License(models.Model):
    """ Model of music license
    """
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name='licenses')
    text = models.TextField(max_length=1000)


class Genre(models.Model):
    """ Model of genre license
    """
    name = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.name


class Album(models.Model):
    """ Model of album for tracks
    """
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name='albums')
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=1000)
    private = models.BooleanField(default=False)
    cover = models.ImageField(
        upload_to=get_path_upload_cover_album,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg']), validate_size_image]
    )


