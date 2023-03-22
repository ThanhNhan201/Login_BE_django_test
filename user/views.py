from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics, permissions
from user.models import MyUser
from django.contrib.auth.models import User
from .serializers import UserSerializer, PasswordResetRequestSerializer, UserSerializerDecode
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from django.views import View
import jwt
from rest_framework.authentication import TokenAuthentication
# Create your views here.


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['id'] = user.id
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    try:
        serializer_class = MyTokenObtainPairSerializer
    except Exception as e:
        print(e)


# POST - /api/users/register
@api_view(['POST'])
def create_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')

    if not username or not password or not email:
        return Response({'error': 'Please provide username, password and email.'},
                        status=status.HTTP_400_BAD_REQUEST)
    try:
        # Create the user object
        user = MyUser.objects.create_user(
            username=username, email=email, password=password)
        user.save()

        return Response({'success': 'User created successfully!'}, status=status.HTTP_201_CREATED)

    except:
        return Response({'error': 'Unable to create user. Please try again.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# POST - /api/users/logout


def index(request):
    return HttpResponse("user")
