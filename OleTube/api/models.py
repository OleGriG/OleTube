from django.db import models
from users.forms import User
from django.core.validators import FileExtensionValidator


class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    video_file = models.FileField(validators=[FileExtensionValidator(['mp4'])])
    likes = models.ManyToManyField(User, related_name='video_likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='video_dislikes', blank=True)
    likes_count = models.IntegerField(default=0)
    dislike_count = models.IntegerField(default=0)
    name = models.CharField(max_length=255, default='')
    #uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
    

class Comment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.content[:20]}"
