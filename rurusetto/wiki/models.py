from django.db import models

RELEASE_TYPE = (
    ('pre-release', 'Pre-release'),
    ('stable', 'Stable')
)


class Changelog(models.Model):
    version = models.TextField(default='', max_length=30)
    time = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=50, choices=RELEASE_TYPE, default='stable')
    note = models.TextField(default='Awesome release notes here!', max_length=5000)

    def __str__(self):
        return f'{self.version} changelog ({self.type})'