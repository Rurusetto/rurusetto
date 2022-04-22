# Generated by Django 4.0.4 on 2022-04-22 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0036_alter_config_theme'),
    ]

    operations = [
        migrations.AlterField(
            model_name='config',
            name='language',
            field=models.TextField(choices=[('en', 'English (Default)'), ('fr', 'French (Not complete)'), ('th', 'Thai')], default='en-EN'),
        ),
    ]
