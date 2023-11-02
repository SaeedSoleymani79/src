from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Book
from .forms import book_form
# Create your views here.

def success_url(request):
    messages.success(request, 'Your data has been saved')
    return redirect('messages.html')

def insert_book(request, *args, **kwargs):
    if request.method == 'POST':
        form = book_form(request.POST)
        if form.is_valid():
            # Create a new instance of book_form
            my_model = Book()
            # Set the fields of my_model 
            # to the values from the form
            my_model.title = form.cleaned_data['title']
            my_model.author = form.cleaned_data['author']
            my_model.description = form.cleaned_data['description']
            my_model.read_states = form.cleaned_data['read_states']

            my_model.save()
            success_url(request)
    else:
        form = book_form()
    return render(request, 'book_create.html', {'form': form})
"""def insert_book(request):
    form = book_form(request.POST or None)
    if form.is_valid():
        form.save()
        form = book_form()
    context = {
        'form': form,
    }

    return render(request, 'book_create.html', context)"""

def home_view(request, *args, **kwargs):

    obj = Book.objects.filter(user=request.user.id)

    context = {
        'book': obj
    }

    return render(request,'home.html', context)

# Remember to learn more about djangp commands and use them to solve problems in Quera.
# For more information go to geeks for geeks and other sources on youtube
# Get all the preparations before the django-python coding match on Quera website 
# 
# An example for django command is manage.py file which is a default that would run default django neccessitiews for a django app to run
# Mute all the necessary offline projects while working on your current project
# Also try to create a unique virtual env for each dajngo project
# 