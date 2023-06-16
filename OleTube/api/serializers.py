from rest_framework import serializers
from .models import Video, Comment
import requests
from django.core.files import File


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Comment
        fields = ('user', 'comment', 'created_at')


class VideoSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()
    dislikes = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Video
        fields = ('id', 'title', 'description', 'video_file', 'likes', 'dislikes', 'comments')

    def get_likes(self, obj):
        return obj.likes.count()

    def get_dislikes(self, obj):
        return obj.dislikes.count()