# Generated by Django 4.2.2 on 2023-06-13 20:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_remove_video_video_file_url_video_video_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='uploaded_by',
        ),
    ]