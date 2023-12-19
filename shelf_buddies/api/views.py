from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from django.views import View
from .forms import RateForm, CommentForm, BookmarkForm
from django.conf import settings
from .models import Books, User_Bookmark, Rate, Comment
from django.db.models import Q
import random
from django.urls import reverse
from authorization.models import Userprofile
#from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
import requests

# Create your views here.

def get_location2(request):
    return render(request, 'index.html')

class BookDetailView(View):
    def get(self, request, *args, **kwargs):
        book_id = kwargs.get('id')
        book = Books.objects.filter(google_books_id=book_id).first()
        rating = Rate.objects.filter(book=book, user=request.user).first()
        comments = Comment.objects.filter(book=book)
        bookmark = User_Bookmark.objects.filter(book=book, user=request.user).first()
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
            'bookmark': bookmark,
        }
        return render(request, 'book_detail2.html', context)
    
def search_books(request):
    title_query = request.GET.get('title')
    author_query = request.GET.get('author')
    results = []

    if title_query or author_query:

        db_results = Books.objects.filter(Q(title__icontains=title_query) | Q(author__icontains=author_query))
        for result in db_results:
            results.append({
                'id': result.google_books_id,
                'title': result.title,
                'author': result.author,
                'isbn': result.isbn,
                'source': 'Database',
            })

        # search based on api
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
                        'source': 'API',
                    })
        except requests.exceptions.RequestException as e:
            # handle error
            print(f"An error occurred: {e}")

    return render(request, "search_books.html", {"results": results})

class BookmarkView(View):
    def get(self, request, *args, **kwargs):
        book_id = kwargs.get('book_id')
        book = get_object_or_404(Books, google_books_id=book_id)
        bookmark, created = User_Bookmark.objects.get_or_create(
            user=request.user,
            book=book,
            defaults={'reading_status': 'WANT_TO_READ', 'reading_progress': 0},
        )
        form = BookmarkForm(instance=bookmark)
        return render(request, 'form.html', {'form': form, 'book': book})

    def post(self, request, *args, **kwargs):
        book_id = request.POST.get('book_id')
        book = get_object_or_404(Books, google_books_id=book_id)
        bookmark, created = User_Bookmark.objects.get_or_create(
            user=request.user,
            book=book,
            defaults={'reading_status': 'WANT_TO_READ', 'reading_progress': 0},
        )
        form = BookmarkForm(request.POST, instance=bookmark)
        if form.is_valid():
            form.save()
            return HttpResponse('Bookmark updated successfully.')
        else:
            return HttpResponse('Invalid data.')
    
def bookmark_view(request, google_books_id):
    book = get_object_or_404(Books, google_books_id=google_books_id)
    bookmark, created = User_Bookmark.objects.get_or_create(
        user=request.user,
        book=book,
        defaults={'reading_status': 'WANT_TO_READ', 'reading_progress': 0},
        )
    print(bookmark)
    if request.method == 'POST':
        form = BookmarkForm(request.POST, instance=bookmark)
        if form.is_valid():
            form.save()
            return redirect('book_detail2', id=book.google_books_id)
    else:
        form = BookmarkForm(instance=bookmark)  # This line populates the form with the saved data

    return render(request, 'form.html', {'form': form, 'bookmark': bookmark})

def delete(request, google_books_id):
    book = get_object_or_404(Books, google_books_id=google_books_id)
    bookmark = get_object_or_404(User_Bookmark, user=request.user, book=book)
    bookmark.delete()
    return redirect('book_detail2', id=book.google_books_id)


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
    bookmarks = User_Bookmark.objects.filter(user__in=following_users)

    # Combine all actions into one list and sort them by date (newest first)
    actions = sorted(
        list(comments) + list(rates) + list(bookmarks),
        key=lambda action: action.created_at,  # Replace with your timestamp field
        reverse=True
    )

    return render(request, 'feed.html', {'actions': actions})

def shelf_view(request):
    response = requests.get('https://www.googleapis.com/books/v1/volumes?q={}&key={}'.format('python', settings.GOOGLE_BOOKS_API_KEY))
    data = response.json()
    for book in data['items']:
        if not Books.objects.filter(google_books_id=book['id']).exists():
            Books.objects.create(
                google_books_id=book['id'],
                title=book['volumeInfo']['title'],
                genre=book['volumeInfo']['categories'][0],
                author=book['volumeInfo']['authors'][0],
                isbn=book['volumeInfo']['industryIdentifiers'][0]['identifier'],
                total_pages=book['volumeInfo']['pageCount'],
                image=book['volumeInfo']['imageLinks']['thumbnail']
            )
    genres = Books.objects.values_list('genre', flat=True).distinct()
    selected_genre = request.GET.get('genre')
    if selected_genre:
        books = Books.objects.filter(genre=selected_genre)
    else:
        books = Books.objects.all()
    context = {
        'books': books,
        'genres': genres,
        'suggested': suggested,
    }
    return render(request, 'shelf.html', context)

def suggested(request):
    user = request.user
    bookmark = User_Bookmark.objects.filter(user=user).values_list('book__genre', flat=True)

    suggested = []


    for genre in bookmark:
        params = {'langRestrict': 'en'}
        response = requests.get(f'https://www.googleapis.com/books/v1/volumes?q=subject:{genre}', params=params)


        if response.status_code == 200:
            data = response.json()
            if 'items' in data:
                # Add the books from the response to the suggested_books list
                suggested.extend(data['items'])

    return render(request, 'suggested.html', {'suggested': suggested})

def author_page(request, author):
    # Replace spaces in the author's name with '+'
    author = author.replace(' ', '+')

    # Send a GET request to the Google Books API
    params = {'langRestrict': 'en'}
    response = requests.get(f'https://www.googleapis.com/books/v1/volumes?q=inauthor:{author}', params=params)

    # Parse the JSON response
    data = response.json()

    # Extract the book data from the response
    books = [item['volumeInfo'] for item in data['items']]
    
    

    # Initialize author_info, author_picture, and author_bio to None
    author_info = None
    author_picture = None
    author_bio = None

    try:
        author_info = books[0]['authors'][0]
        author_picture = books[0]['imageLinks']['thumbnail']
        author_bio = books[0]['description']
    except KeyError:
        pass  # One of the keys was not found, ignore it
    
    book_ids = [book['id'] for book in data['items']]
    book_ids = zip(books, book_ids)

    # Render the author page template with the book data
    return render(request, 'author_page.html', {
        'author': author_info,
        'picture': author_picture,
        'bio': author_bio,
        'books': books,
        'book_ids': book_ids,
    })

def save_random_books(request):
    # Generate a random number of books to fetch (between 1 and 40)
    num_books = random.randint(1, 40)

    # Fetch the data from the Google Books API
    response = requests.get('https://www.googleapis.com/books/v1/volumes?q={}&maxResults={}&langRestrict={}&key={}'.format('random', num_books, 'en', settings.GOOGLE_BOOKS_API_KEY))
    data = response.json()

    # Iterate over the books data
    for book in data['items']:
        # Check if the book already exists in the database
        if not Books.objects.filter(google_books_id=book['id']).exists():
            # If not, create a new Books object and save it to the database
            genre = book['volumeInfo']['categories'][0] if 'categories' in book['volumeInfo'] else 'Unknown'
            total_page = book['volumeInfo']['pageCount'] if 'pageCount' in book['volumeInfo'] else 0
            Books.objects.create(
                google_books_id=book['id'],
                title=book['volumeInfo']['title'],
                genre=genre,
                author=book['volumeInfo']['authors'][0],
                isbn=book['volumeInfo']['industryIdentifiers'][0]['identifier'],
                total_pages=total_page,
                image=book['volumeInfo']['imageLinks']['thumbnail']
            )

    # You can return an HttpResponse here to confirm that the books have been saved
    return HttpResponse('Random books have been saved to the database.')
