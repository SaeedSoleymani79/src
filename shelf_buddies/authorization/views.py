from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.http import Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext as _
import datetime
from .forms import registerForm
from authorization.models import Userprofile, Post
from django.contrib.auth.models import User

# Create your views here.

# Google_authentication is going to use google authenticator as a login or signup tool
# This allows the user to sign up or login using his/her google account

def google_authentication():
    pass

def password_validation(request):
    pass

# login_view() is handling user's login and validation

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print(username, 'has logged in at', datetime.datetime.now() ) # to see who has logged in in cmd
            return redirect('home_view') #redirect(<name of home_page_view in urls.py>)
        else:
            return HttpResponse('Could not log you in')
    
    return render(request, 'authorization/login.html')

def logout_view(request):
    logout(request)
    return redirect("home_view")




# signup_view() will handle registering new users
def signup_view(request):
    if request.method == 'POST':
        form = registerForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Don't commit the save yet
            user.save()  # Explicitly save the user data
            login(request, user)
            return redirect('home_view')
    else:
        form = registerForm()
    return render(request, 'authorization/signup.html', {'form': form})

def terms_view(request):
    return render(request, 'authorization/terms.html')


def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile, created = Userprofile.objects.get_or_create(user=user)

    if created:
        # Set default values for the fields
        profile.followers_count = 0
        profile.books_read_count = 0
        profile.books_want_to_read_count = 0
        profile.books_currently_reading_count = 0
        profile.save()    
    try:
        posts = Post.objects.filter(user=user)
    except Post.DoesNotExist:
        posts = []  # Provide an empty list as a default value when no posts are found

    context = {
        'profile': profile,
        'posts': posts,
    }

    return render(request, 'authorization/user_profile2.html', context)

from django.shortcuts import redirect

def follow_user(request, username):
    if request.user.is_authenticated:
        user_to_follow = User.objects.get(username=username)
        user_profile = Userprofile.objects.get(user=request.user)
        if user_to_follow != request.user:  # Prevent users from following themselves
            user_to_follow.profile.followers.add(request.user)  # Add the follower to the followed user's followers list
        return redirect('profile', username=username)
    else:
        return redirect('login')

def unfollow_user(request, username):
    if request.user.is_authenticated:
        user_to_unfollow = User.objects.get(username=username)
        user_profile = Userprofile.objects.get(user=request.user)
        user_to_unfollow.profile.followers.remove(request.user)  # Remove the follower from the unfollowed user's followers list
        return redirect('profile', username=username)  # Redirect to the user's profile you unfollowed
    else:
        return redirect('login')


def followers_view(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404("User does not exist")
    followers = user.profile.followers.all()
    return render(request, 'authorization/followers.html', {'followers': followers})

def following_view(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        following = user.profile.following.all()
    return render(request, 'authorization/following.html', {'following': following})


    '''
def signup_view(request):

    if request.method == 'GET':
        form = registerForm()
        return render(request, 'signup.html', {'form': form})
    
    if request.method == 'POST':
        form = registerForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login_view(request)
            return redirect('posts')
        else:
            return render(request, 'signup.html', {'form': form})
            '''
