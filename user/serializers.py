from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from user.models import MyUser
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

class UserSerializer(ModelSerializer):
    class Meta:
        model = MyUser
        fields = '__all__'


class blacklistTokenSerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['token']
        return attrs
    
    def save(self, *args, **kwargs):
        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail("Bad token")