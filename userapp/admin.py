from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Post, Follow

CustomUser = get_user_model()

admin.site.register(CustomUser)
admin.site.register(Post)
admin.site.register(Follow)

# Register your models here.
