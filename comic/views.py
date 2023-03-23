from django.core.paginator import Paginator, EmptyPage
from .models import Comic, Genre, Chap
from .serializers import ComicSerializer, ChapSerializer
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import FieldError
from django.utils import timezone
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response


def index(request):
    return HttpResponse("comics")

# GET - api/comics/<sort_field>/<page_num>
def getComicBySortFiled(request, page_num, sort_field):

    try:
    # Get newest chap 
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

            latest_chaps = Chap.objects.filter(comic=comic).order_by('-updated_at')[:3]
            serialized_chap = ChapSerializer(instance=latest_chaps, many=True)

        serialized_comic = {
            'id': comic.id,
            'name': comic.name,
            'created_at': comic.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            'updated_at': comic.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            'view': comic.view,
            'rating': comic.rating,
            'image': comic.image.url,
            'follower': comic.follower, 
            'comment': comic.comment,
            'chap': comic.chap,
            "latest_chaps": serialized_chap.data
            # 'sumary': comic.sumary,
            # 'status': comic.status,
            # 'genres': serialized_genres,
            # 'other_name': comic.other_name,
            # 'author': comic.author,
        }
        serialized_comics.append(serialized_comic)

    return JsonResponse(serialized_comics, safe=False)

# GET - api/comics/<comic_id>
@api_view(['GET'])
def getComicDetail(request, comic_id):
    comic = Comic.objects.get(pk=comic_id)
    if not comic: return JsonResponse({'error': 'Not exist comic'}, status=400)

    serialized_comic = ComicSerializer(instance=comic)

    return Response(serialized_comic.data, status=status.HTTP_200_OK)
