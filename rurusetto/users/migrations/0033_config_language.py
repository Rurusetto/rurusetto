# Generated by Django 4.0.3 on 2022-04-08 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0032_auto_20211011_0942'),
    ]

    operations = [
        migrations.AddField(
            model_name='config',
            name='language',
            field=models.TextField(choices=[('en-EN', 'English (Default)'), ('th', 'Thai')], default='en-EN'),
        ),
    ]
