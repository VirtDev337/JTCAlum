# Generated by Django 4.0.3 on 2022-07-16 23:43

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('name', models.CharField(max_length=200)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(default='', editable=False, max_length=200)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('featured_image', models.ImageField(blank=True, default='projects/default.jpg', null=True, upload_to='projects/')),
                ('demo_link', models.CharField(blank=True, max_length=2000, null=True)),
                ('source_link', models.CharField(blank=True, max_length=2000, null=True)),
                ('demo', models.BooleanField(blank=True, default=False, null=True)),
                ('demo_set', models.BooleanField(blank=True, default=False, null=True)),
                ('project_name', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('site_name', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('project_directory', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('site_directory', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('vote_total', models.IntegerField(blank=True, default=0, null=True)),
                ('vote_ratio', models.IntegerField(blank=True, default=0, null=True)),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.profile')),
                ('site', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='sites.site')),
                ('tags', models.ManyToManyField(blank=True, to='projects.tag')),
            ],
            options={
                'ordering': ['-vote_ratio', '-vote_total', 'title'],
                'unique_together': {('slug', 'owner')},
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('body', models.TextField(blank=True, null=True)),
                ('value', models.CharField(choices=[('up', 'Up Vote'), ('down', 'Down Vote')], max_length=200)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.profile')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project')),
            ],
            options={
                'unique_together': {('owner', 'project')},
            },
        ),
    ]
