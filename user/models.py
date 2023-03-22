from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
# Create your models here.


class MyUser(AbstractUser):
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    avatar_url = models.URLField(blank=True)
    fullname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username


class PasswordResetRequest(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return self.user.username
