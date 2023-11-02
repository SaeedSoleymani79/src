from django.contrib import admin

# Register your models here.

#superuser  = user = raha0837 password = rahashelf

from .models import Book

admin.site.register(Book)