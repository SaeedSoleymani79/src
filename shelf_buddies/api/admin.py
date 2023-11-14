from django.contrib import admin
from .models import Books, User_Bookmark

# Register your models here.

admin.site.register(Books)
admin.site.register(User_Bookmark)