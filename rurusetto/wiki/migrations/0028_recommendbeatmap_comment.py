# Generated by Django 3.2.6 on 2021-08-28 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wiki', '0027_recommendbeatmap'),
    ]

    operations = [
        migrations.AddField(
            model_name='recommendbeatmap',
            name='comment',
            field=models.CharField(default=None, max_length=150),
        ),
    ]
