# Generated by Django 3.2.5 on 2021-07-29 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Changelog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.TextField(default='', max_length=30)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('type', models.CharField(choices=[('pre-release', 'Pre-release'), ('stable', 'Stable')], default='stable', max_length=50)),
                ('note', models.TextField(default='Awesome release notes here!', max_length=5000)),
            ],
        ),
    ]