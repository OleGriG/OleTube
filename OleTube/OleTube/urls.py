from django.contrib import admin
from django.urls import path, include
from api.views import index, video_detail
from users.views import profile


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('auth/', include('users.urls')),
    path('accounts/profile/', profile, name='profile'),
    path('videos/<int:video_id>/', video_detail, name='video_detail'),
    path('', index, name='index'),
]
