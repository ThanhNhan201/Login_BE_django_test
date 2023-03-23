from django.db import models
# Create your models here.
from django.apps import apps

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
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    comic = models.ForeignKey(Comic, on_delete=models.CASCADE, related_name="chapter")
    def __str__(self):
        return f"{self.chap_num} {self.name} {self.comic.name} {self.updated_at}"
