# Generated by Django 3.2.7 on 2021-10-04 14:02

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wiki', '0039_ruleset_github_download_filename'),
    ]

    operations = [
        migrations.AddField(
            model_name='ruleset',
            name='dark_icon',
            field=models.ImageField(default='default_icon.png', upload_to='rulesets_icon_dark', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'gif', 'jpg', 'jpeg', 'bmp', 'svg', 'webp'])]),
        ),
    ]
