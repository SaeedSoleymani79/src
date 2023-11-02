from django.db import models
from django.contrib.auth.models import User
from book.models import Book

# Create your models here.

class Userprofile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(blank=True)
    followers = models.ManyToManyField(User, related_name='following', blank=True)
    books_read = models.ManyToManyField(Book, related_name='read', blank=True)
    books_want_to_read = models.ManyToManyField(Book, related_name='want_to_read', blank=True)
    books_currently_reading = models.ManyToManyField(Book, related_name='currently_reading', blank=True)

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.IntegerField()
    content = models.TextField()