from django.urls import path
from .views import BookDetailView, search_books, rate_view, review_book, bookmark_view

urlpatterns = [
    path('book/<str:id>/', BookDetailView.as_view(), name='book_detail2'),
    path('rate/<str:google_books_id>/', rate_view, name='rate_book'),
    path('review/<str:google_books_id>/', review_book, name='review_book'),
    path('search/', search_books, name='search_books'),
    path('bookmark/<str:google_books_id>/', bookmark_view, name='bookmark'),  # new URL pattern for the BookmarkView
]
