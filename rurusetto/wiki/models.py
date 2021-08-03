from django.core.validators import FileExtensionValidator
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
        return f'{self.version} changelog ({self.type})'


class Ruleset(models.Model):
    creator = models.CharField(default="0", max_length=10)
    owner = models.CharField(default="0", max_length=10)

    name = models.CharField(default="", max_length=20)
    slug = models.SlugField(default="", max_length=20)
    description = models.CharField(default="", max_length=150)
    icon = models.ImageField(default='default_icon.png', upload_to='rulesets_icon', validators=[
        FileExtensionValidator(allowed_extensions=['png', 'gif', 'jpg', 'jpeg', 'bmp', 'svg'])])
    logo = models.ImageField(default='default_logo.jpeg', upload_to='rulesets_logo', validators=[
        FileExtensionValidator(allowed_extensions=['png', 'gif', 'jpg', 'jpeg', 'bmp', 'svg'])])
    cover_image = models.ImageField(default='default_wiki_cover.jpeg', upload_to='wiki_cover', validators=[
        FileExtensionValidator(allowed_extensions=['png', 'gif', 'jpg', 'jpeg', 'bmp', 'svg'])])
    content = models.TextField(default="and awesome content!")

    github_link = models.URLField(default="")

    last_edited_by = models.CharField(default="0", max_length=10)
    last_edited_at = models.DateTimeField(auto_now=True, editable=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.name

