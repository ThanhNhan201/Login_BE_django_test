from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage
from .models import Comic, Genre
from .serializers import ComicSerializer, GenreSerializer
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import FieldError
from django.utils import timezone
from datetime import timedelta, datetime
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

def index(request):
    return HttpResponse("comics")

# GET - api/comics/<sort_field>/<page_num>
def getComicBySortFiled(request, page_num, sort_field):

    try:
        comicsSofted = Comic.objects.all().order_by(sort_field)
        paginator = Paginator(comicsSofted, 10)
        page_comic = paginator.page(page_num)

    except FieldError:
        return JsonResponse({'error': 'Page not found'}, status=404)
    except EmptyPage:
        return JsonResponse({'error': 'Page not found'}, status=404)
    

    serialized_comics = []
    for comic in page_comic:
        serialized_genres = []
        for genre in comic.genres.all():
            serialized_genre = {
                'id': genre.id,
                'name': genre.name,
                'slug': genre.slug
            }
            serialized_genres.append(serialized_genre)

        serialized_comic = {
            'id': comic.id,
            'name': comic.name,
            'other_name': comic.other_name,
            'created_at': comic.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            'updated_at': comic.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            'view': comic.view,
            'rating': comic.rating,
            'author': comic.author,
            'image': comic.image.url,
            'follower': comic.follower,
            'comment': comic.comment,
            'chap': comic.chap,
            'sumary': comic.sumary,
            'status': comic.status,
            'genres': serialized_genres,
        }
        serialized_comics.append(serialized_comic)

    return JsonResponse(serialized_comics, safe=False)

# GET - api/comics/<sort_field>/<sort_date_range>/<page_num>
def top_views_by_date(request):
    date = datetime('2023', '03', '21')
    start_date = timezone.make_aware(date, timezone.get_current_timezone())
    end_date = start_date + timedelta(days=1)

    top_views = Comic.objects.filter(
        created_at__gte=start_date,
        created_at__lt=end_date
    ).order_by('-view')[:10]

    return top_views

 
