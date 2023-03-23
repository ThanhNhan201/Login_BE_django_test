from rest_framework.serializers import ModelSerializer
from comic.models import Comic, Genre, Chap
from rest_framework import serializers

class GenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields = ("name", "slug")
        
class ComicSerializer(ModelSerializer):
    genres = GenreSerializer(many=True)
    class Meta:
        model = Comic
        fields = '__all__'

class ComicSerializerBasicInfo(ModelSerializer):
    newest_chap = serializers.SerializerMethodField()
    class Meta:
        model = Comic
        fields = ["image", "name", "newest_chap"]

    def get_newest_chap(self, obj):
        newest_chap = obj.chapter.order_by('-created_at').first()
        if newest_chap:
            return {
                'name': newest_chap.name,
                'created_at': newest_chap.created_at,
            }
        return None      

class GenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class ChapSerializer(ModelSerializer):
    class Meta:
        model = Chap
        fields = ['updated_at', 'chap_num', 'name']
