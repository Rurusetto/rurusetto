# Generated by Django 3.2.6 on 2021-08-25 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wiki', '0024_alter_subpage_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subpage',
            name='ruleset_id',
            field=models.CharField(default='0', max_length=10),
        ),
    ]
