from django.db import models
from django.contrib.auth.models import User

RELEASE_TYPE = (
    ('pre-release', 'Pre-release'),
    ('stable', 'Stable')
)


class Changelog(models.Model):
    version = models.CharField(default='', max_length=30)
    time = models.DateTimeField(auto_now_add=True)
    type = models.TextField(choices=RELEASE_TYPE, default='stable')
    note = models.TextField(default='Awesome release notes here!')

    def __str__(self):
        return f'{self.version} changelog ({self.type})'m