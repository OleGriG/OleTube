# Generated by Django 4.2.2 on 2023-06-13 17:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_remove_video_video_file_url_video_url_storage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='video',
            old_name='url_storage',
            new_name='video_file_url',
        ),
    ]
