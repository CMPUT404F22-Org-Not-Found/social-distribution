# Generated by Django 4.1.2 on 2022-10-23 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0002_rename_image_author_profileimage_alter_author_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='host',
            field=models.URLField(blank=True, editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='author',
            name='url',
            field=models.URLField(blank=True, editable=False, null=True),
        ),
    ]
