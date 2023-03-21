from django.db import models
# Create your models here.

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
    GENDER = (
        ('male', "male"),
        ('demale', 'female'),
        ('unisex', 'unisex')
    )

    name = models.CharField(max_length=255, null=False)
    other_name = models.CharField(max_length=255, null=False)
    author = models.CharField(max_length=255, null=False)
    created = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="updating", null=False)
    views = models.IntegerField(default=0, null=False)
    sumary = models.CharField(max_length=255, null=False)
    image = models.ImageField(upload_to='comic/', default=None)
    gender = models.CharField(max_length=20, choices=GENDER, default="unisex", null=False)
    rating = models.IntegerField(default=0)
    follower = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    chap = models.IntegerField(default=0)
    genres = models.ManyToManyField(Genre, related_name='comics')

    def __str__(self):
        return self.name
    


    