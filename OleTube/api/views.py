from rest_framework import generics
from .models import Video, Comment
from .serializers import VideoSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
import os
import tempfile
from django.conf import settings
import datetime
from rest_framework import status
from yadisk import YaDisk
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.generic import TemplateView
from users.forms import User


YANDEX_TOKEN = os.getenv('YANDEX_TOKEN')


def index(request):
    videos = get_video_links()
    videos_model = list(Video.objects.all())
    return render(request, 'index.html', {'videos': videos, 'videos_model': videos_model})


def get_video_links():
    y = YaDisk(token=YANDEX_TOKEN)
    files = y.listdir('/videos/')
    links = []
    videos = Video.objects.all()
    id = -1
    for file in files:
        id+=1
        videooo = get_object_or_404(Video, name=file.name)
        link = y.get_download_link(file.path)
        links.append({'name': file.name, 'link': link, 'videooo': videooo})
    return links


class CreateVideoView(generics.CreateAPIView, TemplateView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    template_name = 'video_upload.html'

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        video_file = request.FILES.get('video_file')
        if not video_file:
            return Response({'error': 'No video file provided'}, status=status.HTTP_400_BAD_REQUEST)

        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            for chunk in video_file.chunks():
                temp_file.write(chunk)

        y = YaDisk(token=YANDEX_TOKEN)
        try:
            now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            Video.objects.create(
                title=request.data.get('title'),
                description=request.data.get('description'),
                video_file=request.data.get('video_file'),
                name=now + '_' + video_file.name,
                )
            y.upload(temp_file.name, '/videos/' + now + '_' + video_file.name)
        except Exception as e:
            os.remove(temp_file.name)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        os.remove(temp_file.name)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ListVideoView(generics.ListAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer


class DetailVideoView(generics.RetrieveAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    lookup_field = 'id'


class DeleteVideoView(generics.DestroyAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    lookup_field = 'id'


@login_required
@api_view(['POST'])
def like_video(request, video_id):
    video = Video.objects.get(id=video_id)
    user = User.objects.get(id=request.user.id)
    if user not in video.likes.all():  # проверяем, что пользователь еще не поставил лайк
        video.likes.add(user)
        video.dislikes.remove(user)
        video.likes_count += 1  
        video.save()
        return Response({'message': 'Лайк добавлен'})
    else:
        video.likes.remove(user)
        video.likes_count -= 1  
        video.save()
        return Response({'message': 'лайк убран'})


@login_required
@api_view(['POST'])
def dislike_video(request, id):
    video = Video.objects.get(id=id)
    user = User.objects.get(id=request.user.id)
    if user not in video.likes.all():
        video.likes.remove(user)
        video.dislikes.add(user)
        video.dislike_count += 1
        video.save()
        return Response({'message': 'Дизлайк добавлен'})
    else:
        video.dislikes.remove(user)
        video.dislike_count -= 1
        video.save()
        return Response({'message': 'дизлайк убран'})


@login_required
@api_view(['POST'])
def add_comment(request, id):
    video = Video.objects.get(id=id)
    user = User.objects.get(id=request.user.id)
    content = request.POST.get('content')
    comment = Comment.objects.create(video=video, user=user, content=content)
    return Response({'message': 'Комментарий успешно добавлен'})


def get_likes(request, video_id):
    video = Video.objects.get(id=video_id)
    likes = video.likes.count()
    return JsonResponse({'likes': likes})


def get_dislikes(request, video_id):
    video = Video.objects.get(id=video_id)
    dislikes = video.dislikes.count()
    return JsonResponse({'dislikes': dislikes})


def get_comments(request, video_id):
    video = Video.objects.get(id=video_id)
    comments = [{'user': comment.user.username, 'comment': comment.comment} for comment in video.comments.all()]
    return JsonResponse({'comments': comments})
