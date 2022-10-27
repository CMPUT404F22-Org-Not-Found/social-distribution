# Generated by Django 4.1.2 on 2022-10-26 19:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0004_alter_author_host'),
        ('like', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liked', to='author.author'),
        ),
    ]