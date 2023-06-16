from rest_framework import generics
from .models import Video, Comment
from .serializers import VideoSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
import os
import tempfile
from django.conf import settings
from rest_framework import status
from yadisk import YaDisk
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse


def index(request):
    videos = get_video_links()
    videos_model = list(Video.objects.all())
    return render(request, 'index.html', {'videos': videos, 'videos_model': videos_model})


def get_video_links():
    y = YaDisk(token="y0_AgAAAAA0qF90AAoK0AAAAADlaX_tXppp0ALeQQiANI17xdI3nfpBuds")
    files = y.listdir('/videos/')
    links = []
    id = 7
    for file in files:
        id+=1
        videooo = get_object_or_404(Video, id=id)
        link = y.get_download_link(file.path)
        links.append({'name': file.name, 'link': link, 'videooo': videooo})
    return links


class CreateVideoView(generics.CreateAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    def post(self, request, *args, **kwargs):
        video_file = request.FILES.get('video_file')
        if not video_file:
            return Response({'error': 'No video file provided'}, status=status.HTTP_400_BAD_REQUEST)

        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            for chunk in video_file.chunks():
                temp_file.write(chunk)

        y = YaDisk(token="y0_AgAAAAA0qF90AAoK0AAAAADlaX_tXppp0ALeQQiANI17xdI3nfpBuds")
        try:
            y.upload(temp_file.name, '/videos/' + video_file.name)
        except Exception as e:
            os.remove(temp_file.name)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        os.remove(temp_file.name)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

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


@api_view(['POST'])
def like_video(request, video_id):
    video = Video.objects.get(id=video_id)
    user = request.user
    video.likes.add(user)
    video.dislikes.remove(user)
    video.likes_count += 1  
    video.save()
    return Response({'message': 'Лайк добавлен'})


@api_view(['POST'])
def dislike_video(request, id):
    video = Video.objects.get(id=id)
    user = request.user
    video.likes.remove(user)
    video.dislikes.add(user)
    video.dislike_count += 1
    video.save()
    return Response({'message': 'Дизлайк добавлен'})


@api_view(['POST'])
def add_comment(request, id):
    video = Video.objects.get(id=id)
    user = request.user
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