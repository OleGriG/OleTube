from django.contrib import admin
from django.urls import path, include
from api.views import index
from users.views import profile


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('auth/', include('users.urls')),
    path('accounts/profile/', profile, name='profile'),
    path('', index, name='index'),
]
