from django.http import HttpResponse
from . import views
from django.urls import path
HttpResponse

urlpatterns = [
    path('/', views.index),
]
