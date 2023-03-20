from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from user.models import MyUser
from django.contrib.auth.models import User
from .serializers import UserSerializer, blacklistTokenSerializer
from .utils import get_tokens_for_user
import jwt
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

# Create your views here.

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    try:
        serializer_class = MyTokenObtainPairSerializer
    except Exception as e:
        print(e)

@api_view(['POST'])
def sendEmailResetPassword(request):
    email = request.data.get("email")

    if not email:
        return JsonResponse({'error': 'Please enter email'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = MyUser.objects.get(email=email)
        token = get_tokens_for_user(user)
        return JsonResponse(token)
    except MyUser.DoesNotExist:
        return Response({"message": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
def resetPassword(request):
    token = request.data.get('token')
    resetPassword = request.data.get('password')
    try:
        payload = jwt.decode(token, "secret", algorithms=['HS256'])
        user_id = payload['user_id']
        user = MyUser.objects.get(pk=user_id)

        if not user: return JsonResponse({"message": "Not exist user"}) 
        if not resetPassword: return JsonResponse({"message": "Please enter password"}) 

        user.set_password(resetPassword)
        user.save()
        tokenFormat = RefreshToken(request.data.get('token'), verify=True)
        tokenFormat.blacklist()
      
        return JsonResponse({"message": "Password changed"}, status=status.HTTP_200_OK)
   
    except TokenError as error:
        return JsonResponse({"message": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)
    except jwt.ExpiredSignatureError as error:
        return JsonResponse({"message": str(error.message)})


def index(request):
    return HttpResponse("user")
