# Generated by Django 4.1.2 on 2022-12-04 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='origin',
            field=models.URLField(default='https://cmput404-t04.herokuapp.com/', max_length=500),
        ),
        migrations.AlterField(
            model_name='post',
            name='source',
            field=models.URLField(default='https://cmput404-t04.herokuapp.com/', max_length=500),
        ),
    ]
