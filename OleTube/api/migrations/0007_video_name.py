# Generated by Django 4.2.2 on 2023-06-16 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_video_dislike_count_video_likes_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='name',
            field=models.CharField(default='', max_length=255),
        ),
    ]
