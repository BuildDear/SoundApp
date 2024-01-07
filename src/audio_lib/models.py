from django.db import models

from src.oauth.models import AuthUser


class License(models.Model):
    """ Model of mudic license
    """
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name='licenses')
    text = models.TextField(max_length=1000)

