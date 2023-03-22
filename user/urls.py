from .views import MyTokenObtainPairView
from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('token', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('reset_password', views.sendEmailResetPassword, name='token_refresh'),
    path('create_new_password', views.resetPassword),
    path('register', views.create_user),
    path('comic-follow', views.create_user),
    path('logout', views.logout),
    path('/', views.index),


]
