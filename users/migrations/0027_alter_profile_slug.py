# Generated by Django 4.0.3 on 2022-04-15 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0026_alter_opportunity_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='slug',
            field=models.SlugField(default='', max_length=200),
        ),
    ]