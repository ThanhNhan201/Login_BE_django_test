from datetime import timedelta
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from user.models import MyUser, PasswordResetRequest
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError


class UserSerializer(ModelSerializer):
    class Meta:
        model = MyUser
        fields = '__all__'


class UserSerializerDecode(ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['username', 'id']


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        model = PasswordResetRequest
        fields = '__all__'

    def validate_email(self, value):
        try:
            # print(value)
            user = MyUser.objects.get(email=value)
        except MyUser.DoesNotExist:
            raise ValidationError('No user found with this email address')
        return user

    def create(self, validated_data):
        user = validated_data['email']
        token = RefreshToken.for_user(user).access_token
        expires_at = timezone.now() + timedelta(hours=24)
        PasswordResetRequest.objects.create(
            user=user, token=token, expires_at=expires_at)
        return token
