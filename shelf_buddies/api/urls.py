from django.urls import path
from .views import BookDetailView, get_location2, author_page, search_books, rate_view, review_book, bookmark_view, delete, suggested

urlpatterns = [
    path('book/<str:id>/', BookDetailView.as_view(), name='book_detail2'),
    path('author/<str:author>/', author_page, name='author'),
    path('suggested/', suggested, name='suggested'),
    path('rate/<str:google_books_id>/', rate_view, name='rate_book'),
    path('review/<str:google_books_id>/', review_book, name='review_book'),
    path('search/', search_books, name='search_books'),
    path('bookmark/<str:google_books_id>/', bookmark_view, name='bookmark'),  # new URL pattern for the BookmarkView
    path('bookmark/<str:google_books_id>/delete/', delete, name='delete'),
    path('index/', get_location2),
]
