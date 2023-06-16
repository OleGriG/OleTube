# Generated by Django 4.2.2 on 2023-06-13 17:34

from django.db import migrations
import embed_video.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='video_file_url',
        ),
        migrations.AddField(
            model_name='video',
            name='url_storage',
            field=embed_video.fields.EmbedVideoField(default='https://youtu.be/gKVXaMeazAQ', max_length=500),
        ),
    ]
