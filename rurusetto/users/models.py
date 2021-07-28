from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models
from django.core.exceptions import ValidationError
from .validators import validate_file_size


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpeg', upload_to='profile_pics', validators=[FileExtensionValidator(allowed_extensions=['png', 'gif', 'jpg', 'jpeg'])])
    image = models.ImageField(default='default.jpeg', upload_to='profile_pics', validators=[FileExtensionValidator(allowed_extensions=['png', 'gif', 'jpg', 'jpeg', 'bmp', 'svg'])])
    about_me = models.TextField(default='Hello there!', max_length=120)

    def __str__(self):
        return f'{self.user.username} Profile'

# TODO: Make auto resize picture system


class Config(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} Config'