# Generated by Django 4.0.4 on 2022-06-15 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0018_project_demo_set'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='site_directory',
            field=models.CharField(blank=True, default=models.CharField(blank=True, default='', max_length=200, null=True), max_length=200, null=True),
        ),
    ]
