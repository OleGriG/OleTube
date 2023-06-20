from django.urls import path
from .views import (CreateVideoView, ListVideoView, DetailVideoView,
                    DeleteVideoView, like_video, dislike_video, add_comment,
                    get_comments, get_dislikes, get_likes)

app_name = 'api'

urlpatterns = [
    path('videos/', ListVideoView.as_view(), name='video-list'),
    path('videos/create/', CreateVideoView.as_view(), name='video-create'),
    path('videos/<int:id>/delete/', DeleteVideoView.as_view(), name='video-delete'),
    path('videos/like/<int:video_id>/', like_video, name='like-video'),
    path('videos/<int:id>/dislike/', dislike_video, name='dislike-video'),
    path('videos/<int:id>/comment/', add_comment, name='add-comment'),
    path('videos/<int:video_id>/likes/', get_likes, name='get_likes'),
    path('videos/<int:video_id>/dislikes/', get_dislikes, name='get_dislikes'),
    path('videos/<int:video_id>/comments/', get_comments, name='get_comments'),
]
