from django.urls import path
from django.contrib.auth import views as auth_view
from .views import password_reset, password_reset_done, change_password, password_change_done

urlpatterns = [
    path('password_reset/', 
          password_reset,
          name='password_reset'),
    path('password_reset/done/', 
          password_reset_done, 
          name='password_reset_done'),   
    path('password_change/', 
          change_password,
          name='password_change'), 
    path('password_change/done/', password_change_done, name='password_change_done')
]
