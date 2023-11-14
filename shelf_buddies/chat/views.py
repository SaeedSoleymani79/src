from django.shortcuts import render
from django.contrib.auth.models import User

# Create your views here.

def chatPage(request, *args, **kwargs):
    return render(request, 'chat/chat2.html')