from datetime import timedelta
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from user.models import MyUser, Follow
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from comic.serializers import ComicSerializer, ComicSerializerBasicInfo, ChapSerializer

class UserSerializer(ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('id', 'username', 'email', 'avatar', 'fullname')
 

class FollowSerializer(ModelSerializer):
    comic = ComicSerializerBasicInfo()
    class Meta:
        model = Follow
        fields = ('comic', )
        depth = 1

class FollowSerializerFull(ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'
 