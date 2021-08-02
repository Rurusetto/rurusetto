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
    creator = models.OneToOneField(User, on_delete=models.PROTECT, related_name='%(class)s_page_creator')
    owner = models.OneToOneField(User, on_delete=models.PROTECT, related_name='%(class)s_ruleset_owner')

    name = models.CharField(default="", max_length=20)
    description = models.CharField(default="", max_length=150)
    icon = models.ImageField(default='default_icon.png', upload_to='rulesets_icon', validators=[
        FileExtensionValidator(allowed_extensions=['png', 'gif', 'jpg', 'jpeg', 'bmp', 'svg'])])
    cover_image = models.ImageField(default='default_wiki_cover.jpeg', upload_to='wiki_cover', validators=[
        FileExtensionValidator(allowed_extensions=['png', 'gif', 'jpg', 'jpeg', 'bmp', 'svg'])])
    content = models.TextField(default="and awesome content!")

    open_source = models.BooleanField(default=True)
    github_link = models.URLField(default="")
    last_edited_by = models.OneToOneField(User, on_delete=models.PROTECT, related_name='%(class)s_last_edited_by')
    last_edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} by {self.owner.username}'

