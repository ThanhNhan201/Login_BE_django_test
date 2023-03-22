from .views import MyTokenObtainPairView, PasswordResetView
from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('token', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout', views.blacklist_token, name='logout'),
    path('register', views.create_user),
    path('resetpassword', PasswordResetView.as_view(), name='send-email'),
    path('/', views.index),


]
