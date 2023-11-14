from django.urls import path
from .views import BookDetailView, search_books, BookmarkView

urlpatterns = [
    path('book/<str:id>/', BookDetailView.as_view(), name='book_detail2'),
    path('search/', search_books, name='search_books'),
    path('bookmark/', BookmarkView.as_view(), name='bookmark'),  # new URL pattern for the BookmarkView
]
