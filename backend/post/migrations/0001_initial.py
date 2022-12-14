# Generated by Django 4.1.2 on 2022-11-25 19:42

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('author', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('post_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('id', models.URLField(blank=True, editable=False, max_length=2048, null=True)),
                ('type', models.CharField(default='post', editable=False, max_length=4)),
                ('title', models.CharField(max_length=255, null=True)),
                ('count', models.IntegerField(blank=True, default=0, null=True)),
                ('source', models.URLField(default='http://127.0.0.1:8000/', max_length=500)),
                ('origin', models.URLField(default='http://127.0.0.1:8000/', max_length=500)),
                ('description', models.TextField(blank=True, default='', max_length=255, null=True)),
                ('contentType', models.CharField(choices=[('text/markdown', 'text/markdown'), ('text/plain', 'text/plain'), ('application/base64', 'application/base64'), ('image/png;base64', 'image/png;base64'), ('image/jpeg;base64', 'image/jpeg;base64')], default='text/plain', max_length=30)),
                ('content', models.TextField(blank=True, null=True)),
                ('categories', models.TextField(default='[]', null=True)),
                ('published', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Published')),
                ('visibility', models.CharField(choices=[('PUBLIC', 'PUBLIC'), ('FRIENDS', 'FRIENDS')], default='PUBLIC', max_length=30)),
                ('unlisted', models.BooleanField(default=False)),
                ('url', models.URLField(editable=False, max_length=500, null=True)),
                ('comments', models.URLField(default='<django.db.models.fields.URLField>/comments', editable=False, max_length=500)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_author', to='author.author')),
            ],
        ),
    ]
