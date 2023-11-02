from django.contrib import admin

# Register your models here.

from .models import Userprofile, Post

admin.site.register(Userprofile)
admin.site.register(Post)