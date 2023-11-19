"""
URL configuration for shelf_buddies project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from book.views import home_view
from authorization.views import login_view, logout_view, signup_view, privacy_policy_view,terms_view, profile_view, edit_profile,follow_user, unfollow_user, followers_view , following_view
from api.views import feed_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home_view'),
    path('feed/', feed_view, name='feed_view'),
    path('login/', login_view, name='login_view'),
    path('logout/', logout_view, name='logout'),
    path('profile/<str:username>/', profile_view, name='profile'),
    path('follow/<str:username>/', follow_user, name='follow_user'),
    path('unfollow/<str:username>/', unfollow_user, name='unfollow_user'),
    path('signup/', signup_view, name='signup'),
    path('profile/followers/<str:username>/', followers_view, name='followers'),
    path('profile/following/<str:username>/', following_view, name='following'),
    path('profile/<str:username>/edit_profile/', edit_profile, name='edit_profile'),
    path('terms/', terms_view, name='terms'),
    path('privacy_policy/', privacy_policy_view, name='privacy_policy'),
    path('', include('authorization.urls')),
    path('search/', include('search.urls')),
    path('api/', include('api.urls')),
    path('books/', include('book.urls')),
    path('chat/', include('chat.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)