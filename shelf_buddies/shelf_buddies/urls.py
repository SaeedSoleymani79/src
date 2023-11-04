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
from django.urls import path, include
from book.views import home_view,insert_book,success_url
from authorization.views import login_view, logout_view, signup_view, terms_view, profile_view, follow_user, unfollow_user, followers_view , following_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home_view'),
    path('insert/', insert_book, name='insert_book'),
    path('inser/success', success_url, name='success_url'),
    path('login/', login_view, name='login_view'),
    path('logout/', logout_view, name='logout'),
    path('profile/<str:username>/', profile_view, name='profile'),
    path('follow/<str:username>/', follow_user, name='follow_user'),
    path('unfollow/<str:username>/', unfollow_user, name='unfollow_user'),
    path('signup/', signup_view, name='signup'),
    path('profile/followers/<str:username>/', followers_view, name='followers'),
    path('profile/following/<str:username>/', following_view, name='following'),
    path('terms/', terms_view, name='terms'),
    path('', include('authorization.urls')),
]
