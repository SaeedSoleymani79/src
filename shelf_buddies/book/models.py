from django.db import models
from django.contrib.auth.models import User

class UserBookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    google_books_id = models.CharField(max_length=20)  # Use the same length as in Book model
    status_choices = (
        ('want_to_read', 'Want to Read'),
        ('currently_reading', 'Currently Reading'),
        ('already_read', 'Already Read'),
    )
    status = models.CharField(max_length=20, choices=status_choices)

    def __str__(self):
        return f"{self.user.username} - {self.google_books_id} ({self.status})"
