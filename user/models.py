from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
# Create your models here.


class MyUser(AbstractUser):
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    avatar = models.ImageField(
        upload_to='avatar/', default='avatar/default.jpg')
    fullname = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.username} {self.is_active}"
