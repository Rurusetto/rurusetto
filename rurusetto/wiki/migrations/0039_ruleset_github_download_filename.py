# Generated by Django 3.2.7 on 2021-09-23 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wiki', '0038_auto_20210921_1230'),
    ]

    operations = [
        migrations.AddField(
            model_name='ruleset',
            name='github_download_filename',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]
