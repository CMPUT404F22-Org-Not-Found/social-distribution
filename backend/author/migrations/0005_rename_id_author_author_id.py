# Generated by Django 4.1.2 on 2022-11-22 03:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0004_alter_author_host'),
    ]

    operations = [
        migrations.RenameField(
            model_name='author',
            old_name='id',
            new_name='author_id',
        ),
    ]