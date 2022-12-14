# Generated by Django 4.1.2 on 2022-11-25 19:42

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('author', '0001_initial'),
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('comment_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('id', models.URLField(blank=True, editable=False, max_length=2048, null=True)),
                ('type', models.CharField(default='comment', editable=False, max_length=7)),
                ('comment', models.TextField()),
                ('contentType', models.CharField(choices=[('text/markdown', 'text/markdown'), ('text/plain', 'text/plain'), ('application/base64', 'application/base64'), ('image/png;base64', 'image/png;base64'), ('image/jpeg;base64', 'image/jpeg;base64')], default='text/plain', max_length=30)),
                ('published', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Published')),
                ('url', models.URLField(blank=True, editable=False, max_length=500, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='author.author')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_comment', to='post.post')),
            ],
        ),
    ]
