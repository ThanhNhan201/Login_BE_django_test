from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from comic.models import Comic
# Create your models here.

class MyUser(AbstractUser):
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    avatar = models.ImageField(upload_to='avatar/', default='avatar/default.jpg')
    fullname = models.CharField(max_length=255)
    
    def __str__(self):
        return self.username

class Follow(AbstractUser):
    unfollow = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='followers')   
    comic = models.ForeignKey(Comic, on_delete=models.CASCADE, related_name='follow_comic')
    updated_at = models.DateTimeField(auto_now=True)
