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

    # def get_latest_chaps(self, obj):
    #     latest_chaps = obj.latest_chaps
    #     if latest_chaps:
    #         return [
    #             {
    #                 'id': chap['id'],
    #                 'name': chap['name'],
    #                 'chap_num': chap['chap_num'],
    #                 'created_at': chap['created_at'],
    #                 'updated_at': chap['updated_at'],
    #             }
    #             for chap in latest_chaps
    #         ]
    #     else:
    #         return None

class GenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class ChapSerializer(ModelSerializer):
    class Meta:
        model = Chap
        fields = ['updated_at', 'chap_num', 'name']
