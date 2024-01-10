from datetime import datetime, timedelta

from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import FileExtensionValidator
from django.db import models
import jwt

from SoundApplication import settings
from src.base.services import get_path_upload_avatar, validate_size_image


class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None):

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class AuthUser(models.Model):
    """ User model on my platform
    """
    email = models.EmailField(max_length=150, unique=True)
    password = models.CharField(null=False, max_length=128)
    join_date = models.DateField(auto_now_add=True)
    country = models.CharField(max_length=30, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    bio = models.TextField(max_length=1500, blank=True, null=True)
    display_name = models.CharField(max_length=30, blank=True, null=True)
    avatar = models.ImageField(
        upload_to=get_path_upload_avatar,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg']), validate_size_image]
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def is_authenticated(self):
        return True

    # For custom auth
    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=1)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')


class Follower(models.Model):
    """ Model of subscribers
    """
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name='owner')
    subscriber = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name='subscribers')

    def __str__(self):
        return f'{self.subscriber} subscribe on {self.user}'


class SocialLink(models.Model):
    """ Model links on social network of user
    """
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name='social_links')
    link = models.URLField(max_length=100)

    def __str__(self):
        return f'self.user'
