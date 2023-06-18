from django.contrib.auth.views import LogoutView, LoginView, PasswordResetView
from django.urls import path, include
from . import views

app_name = 'users'

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path(
        'logout/',
        LogoutView.as_view(template_name='logged_out.html'),
        name='logout'
    ),
    path(
        'login/',
        LoginView.as_view(template_name='login.html'),
        name='login'
    ),
    path(
        'password_reset',
        PasswordResetView.as_view(),
        name='password_reset_form'
    ),
]
