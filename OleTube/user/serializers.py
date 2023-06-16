from rest_framework import serializers
from .models import User


class UserRegisterSerializer(serializers.ModelSerializer):


    class Meta:
        model = User
        fields = ['email', 'username', 'password', ]

    def save(self, *args, **kwargs):
        user = User(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
        )
        password = self.validated_data['password']
        user.set_password(password)
        user.save()
        return user
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'id']