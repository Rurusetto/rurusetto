# Generated by Django 3.2.8 on 2021-10-08 20:12

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wiki', '0047_ruleset_cover_image_light'),
    ]

    operations = [
        migrations.AddField(
            model_name='ruleset',
            name='custom_css',
            field=models.ImageField(blank=True, default='', upload_to='custom_css', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['css'])]),
        ),
    ]