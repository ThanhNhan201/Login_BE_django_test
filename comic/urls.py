from django.urls import path
from . import views
from django.http import HttpResponse

urlpatterns = [
    path('/', views.index),
    path('/<str:sort_field>/<int:page_num>', views.getComicBySortFiled ),
]
 