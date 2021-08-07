from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpeg', upload_to='profile_pics', validators=[FileExtensionValidator(allowed_extensions=['png', 'gif', 'jpg', 'jpeg', 'bmp', 'svg', 'webp'])])
    cover = models.ImageField(default='default_cover.png', upload_to='cover_pics', validators=[FileExtensionValidator(allowed_extensions=['png', 'gif', 'jpg', 'jpeg', 'bmp', 'svg', 'webp'])])
    about_me = models.TextField(default='Hello there!', max_length=120)
    osu_username = models.CharField(default='', max_length=20)
    osu_id = models.IntegerField(default='')
    location = models.CharField(default='', max_length=20)
    interests = models.CharField(default='', max_length=20)
    occupation = models.CharField(default='', max_length=20)
    twitter = models.CharField(default='', max_length=20)
    discord = models.CharField(default='', max_length=20)
    website = models.URLField(default='')
    oauth_first_migrate = models.BooleanField(default=False)
    social_account = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} Profile'

# TODO: Make auto resize picture system


class Config(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} Config'