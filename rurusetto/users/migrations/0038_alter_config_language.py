# Generated by Django 4.1.1 on 2023-02-07 02:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0037_alter_config_language'),
    ]

    operations = [
        migrations.AlterField(
            model_name='config',
            name='language',
            field=models.TextField(choices=[('en', 'English (Default)'), ('es', 'Spanish'), ('fr', 'French (Not complete)'), ('th', 'Thai')], default='en-EN'),
        ),
    ]
