from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
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
    
class Rate(models.Model):
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rate = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('book', 'user')

    def __str__(self):
        return str(self.rate)

class User_Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

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

    def __str__(self):
        return self.user.username + ' bookmarked '+ self.book.title + ' as ' + self.reading_status
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    review = models.TextField(blank=True, max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

