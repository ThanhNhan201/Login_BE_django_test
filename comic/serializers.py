from rest_framework.serializers import ModelSerializer
from comic.models import Comic, Genre, Chap

class GenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields = ("name", "slug")
        
class ComicSerializer(ModelSerializer):
    genres = GenreSerializer(many=True)
    class Meta:
        model = Comic
        fields = '__all__'

class GenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class ChapSerializer(ModelSerializer):
    class Meta:
        model = Chap
        fields = '__all__'
