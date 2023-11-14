from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ChatRoom(models.Model):
    user1 = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='user1')
    user2 = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='user2')
    room_name = models.CharField(max_length=128, unique=True)

class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)