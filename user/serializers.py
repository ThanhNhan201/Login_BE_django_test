from datetime import timedelta
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from user.models import MyUser
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class UserSerializer(ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('id', 'username', 'email', 'avatar', 'fullname')
