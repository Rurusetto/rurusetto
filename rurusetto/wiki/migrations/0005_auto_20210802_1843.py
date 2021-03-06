# Generated by Django 3.2.5 on 2021-08-02 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wiki', '0004_alter_ruleset_cover_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='ruleset',
            name='github_link',
            field=models.URLField(default=''),
        ),
        migrations.AlterField(
            model_name='ruleset',
            name='description',
            field=models.CharField(default='', max_length=150),
        ),
        migrations.AlterField(
            model_name='ruleset',
            name='name',
            field=models.CharField(default='', max_length=20),
        ),
    ]
