from django.db import models
# Create your models here.
from django.apps import apps
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator

class Genre(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    
    def __str__(self):
        return self.name
    
class Comic(models.Model):
    STATUS_CHOICES = (
        ("updating", "updating"),
        ("deleted", "deleted"),
        ("ended", "ended"),
    )
    GENDER_CHOICES = (
        ('male', "male"),
        ('demale', 'female'),
        ('unisex', 'unisex')
    )

    name = models.CharField(max_length=255, null=False)
    other_name = models.CharField(max_length=255, blank=True)
    author = models.CharField(max_length=255, null=False, default=None)
    sumary = models.CharField(max_length=255, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, default='unisex')
    image = models.ImageField(upload_to='comic/', null=True)
    rating = models.FloatField(default=0, null=False)
    follower = models.IntegerField(default=0, null=False) 
    comment = models.IntegerField(default=0, null=False)
    chap = models.IntegerField(default=0, null=False)
    view = models.IntegerField(default=0, null=False)
    view_day = models.IntegerField(default=0, null=False)
    view_week = models.IntegerField(default=0, null=False)
    view_month = models.IntegerField(default=0, null=False)
    genres = models.ManyToManyField(Genre)

    def __str__(self):
        return f"{self.id} {self.name} {self.view} {self.chap} {self.rating} {self.updated_at} {self.created_at} {self.status}"
    
class Chap(models.Model):
    chap_num = models.IntegerField(blank=False)
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    comic = models.ForeignKey(Comic, on_delete=models.CASCADE, related_name="chapter")
    images = ArrayField(models.ImageField(upload_to='comic_img/'), null=True)
    def __str__(self):
        return f"{self.chap_num} {self.name} {self.comic.name} {self.updated_at}"

# class ChapImage(models.Model):
#     chap = models.ForeignKey(Chap, editable=False, on_delete=models.CASCADE)
#     images = models.ImageField(upload_to='comic_img/')
#
#     def __str__(self):
#         return self.chap.name


class Comment(models.Model):
    comic = models.ForeignKey(Comic,  related_name='comic', editable=False, on_delete=models.CASCADE)
    chap = models.ForeignKey(Chap, editable=False, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    removed = models.BooleanField(default=False)
    edited = models.BooleanField(default=False)

    def __str_(self):
        return str(self.comic)

class Rating (models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False, on_delete=models.CASCADE)
    comic = models.ForeignKey(Comic, related_name='comic_id', editable=False, on_delete=models.CASCADE)
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    removed = models.BooleanField(default=False)

    class Meta:
        unique_together = (('user', 'comic'),)
        index_together = (('user', 'comic'),)

    def __str__(self):
        return f'{self.user} - {self.comic}'
