from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from django.views import View
from .forms import RateForm, CommentForm
from django.conf import settings
from .models import Books, User_Bookmark, Rate, Comment

from authorization.models import Userprofile
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import requests

# Create your views here.

class BookDetailView(View):
    def get(self, request, *args, **kwargs):
        book_id = kwargs.get('id')
        book = Books.objects.filter(google_books_id=book_id).first()
        rating = Rate.objects.filter(book=book, user=request.user).first()
        comments = Comment.objects.filter(book=book)
        if not book:
            response = requests.get(f'https://www.googleapis.com/books/v1/volumes/{book_id}?key={settings.GOOGLE_BOOKS_API_KEY}')
            data = response.json()

            volume_info = data['volumeInfo']
            book = Books()
            book.google_books_id = book_id
            book.title = volume_info.get('title', '')
            book.author = volume_info.get('authors', [''])[0]
            book.isbn = volume_info.get('industryIdentifiers', [{'identifier': ''}])[0]['identifier']
            book.total_pages = volume_info.get('pageCount', 0)
            image_links = volume_info.get('imageLinks', {'thumbnail': ''})
            book.image = image_links.get('thumbnail', '')
            # Assuming the genre is the first category provided by the API
            book.genre = volume_info.get('categories', [''])[0]
            book.save()


        context = {
            'book': book,
            'rating': rating,
            'comments': comments,
        }
        return render(request, 'book_detail2.html', context)
    
def search_books(request):
    title_query = request.GET.get('title')
    author_query = request.GET.get('author')
    results = []

    if title_query or author_query:
        base_url = "https://www.googleapis.com/books/v1/volumes"

        # Construct the query based on title and/or author
        query_parts = []
        if title_query:
            query_parts.append(f'intitle:{title_query}')
        if author_query:
            query_parts.append(f'inauthor:{author_query}')

        params = {
            "q": '+'.join(query_parts),
            "maxResults": 40,
            "printType": "books",
            "key": settings.GOOGLE_BOOKS_API_KEY,
            "langRestrict": "en"
        }

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()

            books = data.get("items", [])
            books.sort(key=lambda book: (
                book["volumeInfo"].get("averageRating", 0),
                book["volumeInfo"].get("ratingsCount", 0)
            ), reverse=True)

            for item in books:
                volume_info = item.get("volumeInfo", {})
                if "title" in volume_info and "authors" in volume_info and "industryIdentifiers" in volume_info:
                    title = volume_info["title"]
                    authors = ", ".join(volume_info["authors"])
                    isbn = volume_info["industryIdentifiers"][0]["identifier"]
                    
                    book_id = item['id']

                    results.append({
                        'title': title,
                        'authors': authors,
                        'isbn': isbn,
                        'id': book_id,
                    })
        except requests.exceptions.RequestException as e:
            # handle error
            print(f"An error occurred: {e}")

    return render(request, "search_books.html", {"results": results})

class BookmarkView(View):
    def post(self, request, *args, **kwargs):
        book_id = request.POST.get('book_id')
        reading_status = request.POST.get('reading_status')
        reading_progress = request.POST.get('reading_progress', 0)
        book = get_object_or_404(Books, google_books_id=book_id)
        bookmark, created = User_Bookmark.objects.get_or_create(
            user=request.user,
            book=book,
            defaults={'reading_status': reading_status, 'reading_progress': reading_progress},
        )
        if not created:
            bookmark.reading_status = reading_status
            bookmark.reading_progress = reading_progress
            bookmark.save()
        return HttpResponse('Bookmark updated successfully.')
    

@login_required
def rate_view(request, google_books_id):
    book = get_object_or_404(Books, google_books_id=google_books_id)
    user = request.user
    rating, created = Rate.objects.get_or_create(book=book, user=user)

    if request.method == 'POST':
        form = RateForm(request.POST, instance=rating)
        if form.is_valid():
            form.save()
            return redirect('book_detail2', id=book.google_books_id)  # or wherever you want to redirect after form submission
    else:
        form = RateForm(instance=rating)

    return render(request, 'rate.html', {'form': form})

@login_required
def review_book(request, google_books_id):
    book = get_object_or_404(Books, google_books_id=google_books_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.book = book
            comment.save()
            return redirect('book_detail2', id=google_books_id)
    else:
        form = CommentForm()
    return render(request, 'review.html', {'form': form})

@login_required
def feed_view(request):
    # Get the users that the current user is following
    following_users = request.user.profile.following.all()

    # Get the actions of the users that the current user is following
    comments = Comment.objects.filter(user__in=following_users)
    rates = Rate.objects.filter(user__in=following_users)
    # bookmarks = User_Bookmark.objects.filter(user__in=following_users)

    # Combine all actions into one list and sort them by date (newest first)
    actions = sorted(
        list(comments) + list(rates), #+ list(bookmarks),
        key=lambda action: action.created_at,  # Replace with your timestamp field
        reverse=True
    )

    return render(request, 'feed.html', {'actions': actions})
