from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Userprofile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_image = models.ImageField(blank=True, default='image.png')
    # genres = models
    profile_bio = models.TextField(max_length=255, blank=True)
    followers = models.ManyToManyField(User, related_name='followed_by', blank=True)
    following = models.ManyToManyField(User, related_name='following', blank=True)

