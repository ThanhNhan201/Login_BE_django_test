from django.urls import path
from . import views
from django.http import HttpResponse
from .views import CommentAPI, RateViewAPI

urlpatterns = [
    path('/', views.index),
    path('/<int:comic_id>', views.getComicDetail),
    # path('/cmt/<int:comic_id>', views.GetComment),
    path('/cmt/<int:id>/<int:id_chap>', CommentAPI.as_view()),
    path('/rate/<int:comic_id>', RateViewAPI.as_view()),
    path('/put_cmt/<int:comic_id>/<int:cmt_id>', views.PutComment),
    path('/<str:sort_field>/<int:page_num>', views.getComicBySortFiled )
]
 