# Generated by Django 4.1.2 on 2022-11-23 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0007_auto_20221122_0358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='host',
            field=models.URLField(blank=True, default='http://127.0.0.1:8000/', editable=False, null=True),
        ),
    ]
