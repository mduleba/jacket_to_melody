# Generated by Django 4.2.3 on 2023-07-29 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('to_melody', '0004_song_drawn'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='author',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
