# Generated by Django 4.1.2 on 2022-10-25 18:45

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0004_alter_author_host'),
        ('followers', '0004_alter_followrequest_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='FreindRequest',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('type', models.CharField(default='Follow', editable=False, max_length=6)),
                ('summary', models.CharField(max_length=100)),
                ('actor', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='sent_friend_request', to='author.author')),
                ('object', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='recieved_friend_request', to='author.author')),
            ],
        ),
        migrations.DeleteModel(
            name='FollowRequest',
        ),
        migrations.AddConstraint(
            model_name='freindrequest',
            constraint=models.UniqueConstraint(fields=('actor', 'object'), name='unique_friend_request'),
        ),
    ]
