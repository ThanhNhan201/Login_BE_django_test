from django.contrib import admin
from .models import MyUser
# Register your models here.
# admin.site.register(MyUser)
# admin.site.register(Follow)


class MyUserAdmin(admin.ModelAdmin):
    list_display = ("username", "is_active")


admin.site.register(MyUser, MyUserAdmin)
