from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpeg', upload_to='profile_pics')
    about_me = models.TextField(default='Hello there!', max_length=120)

    def __str__(self):
        return f'{self.user.username} Profile'

# TODO: Make auto resize picture system


class Config(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} Config'