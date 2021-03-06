# Generated by Django 3.2.7 on 2021-10-05 17:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wiki', '0043_merge_20211005_1701'),
    ]

    operations = [
        migrations.CreateModel(
            name='RulesetStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latest_version', models.CharField(blank=True, default='', max_length=200)),
                ('latest_update', models.DateTimeField(blank=True)),
                ('changelog', models.TextField(blank=True)),
                ('file_size', models.IntegerField(blank=True, default=0)),
                ('playable', models.TextField(choices=[('yes', 'Yes'), ('no', 'No'), ('unknown', 'Unknown')], default='unknown')),
                ('ruleset', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='wiki.ruleset')),
            ],
        ),
    ]
