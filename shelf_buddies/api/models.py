from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Books(models.Model):
    google_books_id = models.CharField(max_length=200, unique=True, null=True, blank=True)
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=100)
    total_pages = models.IntegerField()
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.title
    

class User_Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    READING_STATUS_CHOICES = [
        ('WANT_TO_READ', 'Want to Read'),
        ('CURRENTLY_READING', 'Currently Reading'),
        ('ALREADY_READ', 'Already Read'),
    ]
    reading_status = models.CharField(max_length=20, choices=READING_STATUS_CHOICES, default='WANT_TO_READ')
    reading_progress = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.reading_status == 'ALREADY_READ':
            self.reading_progress = self.book.total_pages
        super().save(*args, **kwargs)