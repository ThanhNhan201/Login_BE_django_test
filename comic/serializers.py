from rest_framework.serializers import ModelSerializer
from comic.models import Comic, Genre

class GenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields = ("name", "slug")
        
class ComicSerializer(ModelSerializer):
    genres = GenreSerializer(many=True)
    class Meta:
        model = Comic
        fields = '__all__'
       