from django.urls import path
from .views import search_books, book_detail, book_mark

urlpatterns = [
    path('bookmark/<str:google_books_id>/<slug:book_slug>//', book_mark, name='bookmark'),
    path('search/', search_books, name='search_books'),
    path('<str:book_id>/<slug:book_slug>/', book_detail, name='book_detail'),
]
