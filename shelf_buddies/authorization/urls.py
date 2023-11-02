from django.urls import path
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('password_reset/', 
          auth_view.PasswordResetView.as_view(),
          name='password_reset'),
    path('password_reset/done/',
          auth_view.PasswordResetDoneView.as_view(), 
          name='password_reset_done'),
    path('reset/<uibd64>/<token>',
          auth_view.PasswordResetConfirmView.as_view(),
          name='password_reset_confirm'),
    path('reset/done/', 
          auth_view.PasswordResetCompleteView.as_view(), 
          name='password_reset_complete'),
]
