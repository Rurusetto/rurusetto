# Generated by Django 3.2.5 on 2021-07-25 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='about_me',
            field=models.TextField(default='Hello there!', max_length=120),
        ),
    ]
