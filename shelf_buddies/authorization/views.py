from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.urls import reverse
from django.http import Http404
from .decorators import anonymous_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext as _
import datetime
from api.models import User_Bookmark, Books
from .forms import registerForm, UserUpdateForm, UserUpdateProfileForm, CustomPasswordResetForm, CustomChangePasswordForm
from authorization.models import Userprofile
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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
            return redirect(reverse('profile', kwargs={'username':username})) #redirect(<name of home_page_view in urls.py>)
        else:
            return HttpResponse('Could not log you in')
    
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect("home_view")

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Userprofile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


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
    return render(request, 'signup.html', {'form': form})

def terms_view(request):
    return render(request, 'terms.html')

def privacy_policy_view(request):
    return render(request, 'privacy_policy.html')

def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile, created = Userprofile.objects.get_or_create(user=user)

    if created:
        # Set default values for the fields
        profile.followers_count = 0
        profile.save()    

    # Fetch the books that the user has bookmarked based on their reading status
    reading_books = Books.objects.filter(user_bookmark__user=user, user_bookmark__reading_status='CURRENTLY_READING')
    want_to_read_books = Books.objects.filter(user_bookmark__user=user, user_bookmark__reading_status='WANT_TO_READ')
    already_read_books = Books.objects.filter(user_bookmark__user=user, user_bookmark__reading_status='ALREADY_READ')


    context = {
        'profile': profile,
        'reading_books': reading_books,
        'want_to_read_books': want_to_read_books,
        'already_read_books': already_read_books,
    }

    return render(request, 'user_profile2.html', context)

def edit_profile(request, username):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserUpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect(reverse('profile', args=[request.user.username]))
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserUpdateProfileForm(instance=request.user.profile)
    return render(request, 'edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})

def follow_user(request, username):
    if request.user.is_authenticated:
        user_to_follow = User.objects.get(username=username)
        user_profile = Userprofile.objects.get(user=request.user)
        if user_to_follow != request.user:  # Prevent users from following themselves
            user_to_follow.profile.followers.add(request.user)  # Add the follower to the followed user's followers list
            user_profile.following.add(user_to_follow)  # Add the followed user to the follower's following list
            user_profile.following_count = user_profile.following.count()  # Update the following count
            user_profile.save()
        return redirect('profile', username=username)
    else:
        return redirect('login')

def unfollow_user(request, username):
    if request.user.is_authenticated:
        user_to_unfollow = User.objects.get(username=username)
        user_profile = Userprofile.objects.get(user=request.user)
        user_to_unfollow.profile.followers.remove(request.user)  # Remove the follower from the unfollowed user's followers list
        user_profile.following.remove(user_to_unfollow)  # Remove the unfollowed user from the follower's following list
        user_profile.following_count = user_profile.following.count()  # Update the following count
        user_profile.save()
        return redirect('profile', username=username)  # Redirect to the user's profile you unfollowed
    else:
        return redirect('login')

def followers_view(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404("User does not exist")
    followers = user.profile.followers.all()
    return render(request, 'followers.html', {'followers': followers})

def following_view(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        following = user.profile.following.all()
    return render(request, 'following.html', {'following': following})


@anonymous_required(redirect_url='/')
def password_reset(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('password_reset_done')
    else:
        form = CustomPasswordResetForm()
    return render (request, 'password_reset_form.html', {'form': form})
    
def password_reset_done(request):
    return render(request, 'password_reset_done.html')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('password_change_done')
    else:
        form = CustomChangePasswordForm(request.user)
    return render(request, 'password_change_form.html', {'form': form})

def password_change_done(request):
    return render(request, 'password_change_done.html')
