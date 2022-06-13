# Generated by Django 4.0.4 on 2022-06-01 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0014_project_demo'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='app_name',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='project_name',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='site_name',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
    ]
