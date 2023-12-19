from django.contrib import admin
from .models import Books, User_Bookmark, Rate, Comment

# Register your models here.

admin.site.register(Books)
admin.site.register(User_Bookmark)
admin.site.register(Rate)
admin.site.register(Comment)