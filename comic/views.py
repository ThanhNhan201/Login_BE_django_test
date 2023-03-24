from django.core.paginator import Paginator, EmptyPage
from .models import Comic, Genre, Chap, Comment, Rating
from .serializers import ComicSerializer, ChapSerializer, CommentSerializer, CommentPostSerializer
from .serializers import CommentPutSerializer, RatingSerializer
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import FieldError
from django.utils import timezone
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Avg


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


######## COMMENT ###########
class CommentAPI(generics.ListCreateAPIView):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentPostSerializer
    def get(self, request, id, id_chap):
        # user = request.user.username
        comments = Comment.objects.filter(comic=id, removed=False).order_by('-created_at')
        serializer_comment = CommentSerializer(comments, many=True)
        return Response(serializer_comment.data, status=200)

    def post(self, request, id, id_chap):
        comics = Comic.objects.get(id=id)
        content = request.data.get('content')
        if request.user.is_authenticated:
            user = request.user
            data = Comment.objects.create(
                user=user,
                comic_id=id,
                chap_id=id_chap,
                content=content,
            )
            data.save()
            serializer_comment = CommentPostSerializer(data=data)
            if serializer_comment.is_valid():
                serializer_comment.save()
                comics.comment = comics.comment + 1
                comics.save()
            return Response(serializer_comment.data, status=status.HTTP_201_CREATED)
        return Response({'msg': 'user not authenticated'})

#1 fields content can update
@api_view(['PUT', 'DELETE'])
def PutComment(request, comic_id, cmt_id):
    if request.method == 'PUT':
        try:
            cmt = Comment.objects.get(comic=comic_id, id=cmt_id)
            if (cmt.removed == True):
                return Response({'msg': 'this comment was deleted'}, status=400)
        except cmt.DoesNotExist:
            return Response({'msg': 'this comment not found'}, status=400)
        if request.user.is_authenticated:
            cmt.edited = True
            serializer = CommentPutSerializer(cmt, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=200)
            return Response(serializer.errors, status=400)
        return Response({'msg': 'user not authenticated'})

    elif request.method == 'DELETE':
        try:
            cmt = Comment.objects.get(comic=comic_id, id=cmt_id)
            if(cmt.removed == True):
                return Response({'msg': 'this comment was deleted'}, status=400)
        except cmt.DoesNotExist:
            return Response({'msg': 'this comment not found'}, status=400)
        if request.user.is_authenticated:
            cmt.removed = True
            serializer_comment = CommentSerializer(data=cmt)
            if serializer_comment.is_valid():
                serializer_comment.save()
            cmt.save()
            return Response({'msg': 'deleted'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'msg': 'user not authenticated'})

class RateViewAPI(generics.ListCreateAPIView):
    queryset = Rating.objects.filter(removed=False).order_by('-created_at')
    serializer_class = RatingSerializer
    def post(self, request, comic_id):
        stars = request.data.get('stars')
        if request.user.is_authenticated:
            user = request.user
            data = Rating.objects.create(
                user=user,
                comic_id=comic_id,
                stars=stars,
            )
            data.save()
            serializer_rating = RatingSerializer(data=data)
            if serializer_rating.is_valid():
                serializer_rating.save()
                return Response(serializer_rating.data, status=200)
            # return Response(serializer_rating.data, status=status.HTTP_400_BAD_REQUEST)
        return Response({'msg': 'user not authenticated'})
    def get(self, request, comic_id):
        comics = Comic.objects.get(id=comic_id)
        rates = Rating.objects.filter(comic=comic_id, removed=False).aggregate(Avg('stars'))['stars__avg']
        comics.rating = rates
        print(comics.rating)
        comics.save()
        return Response(rates, status=200)



