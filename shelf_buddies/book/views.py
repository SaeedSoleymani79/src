from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import UserBookmark
from django.http import JsonResponse

from django.conf import settings
# Create your views here.

def success_url(request):
    messages.success(request, 'Your data has been saved')
    return redirect('messages.html')

def home_view(request, *args, **kwargs):
    return render(request,'home.html')

import requests
from django.utils.text import slugify
def search_books(request):
    query = request.GET.get('q')
    results = []

    if query:
        base_url = "https://www.googleapis.com/books/v1/volumes"

        params = {
            "q": query,
            "maxResults": 10,
            "printType": "books",
            "key": settings.GOOGLE_BOOKS_API_KEY,
            "langRestrict": "en"
        }

        response = requests.get(base_url, params=params)

        data = response.json()

        books = data.get("items", [])
        books.sort(key=lambda book: book["volumeInfo"].get("ratingCount", 0), reverse=True)

        for item in data['items']:
            volume_info = item.get("volumeInfo", {})
            if "title" in volume_info and "authors" in volume_info and "industryIdentifiers" in volume_info:
                title = item["volumeInfo"]["title"]
                authors = ", ".join(item["volumeInfo"]["authors"])
                isbn = item["volumeInfo"]["industryIdentifiers"][0]["identifier"]
                
                book_slug = slugify(title)
                book_id = item['id']

                results.append({
                    'title': title,
                    'authors': authors,
                    'isbn': isbn,
                    'id': book_id,
                    'slug': book_slug
                })

    return render(request, "search_books.html", {"results": results})

def book_detail(request, book_id, book_slug):
    # Define the base URL for the Google Books API
    base_url = "https://www.googleapis.com/books/v1/volumes/"

    # Send a GET request to the Google Books API
    response = requests.get(base_url + str(book_id) )

    # Check if the response is empty or contains an error
    if response.status_code == 200:
        # Convert the response to JSON
        book = response.json()

        # Render the book details in a template
        return render(request, 'book_detail.html', {'book': book})
    else:
        # Render an error page or message
        return render(request, 'error.html', {
            'message': 'Book not found.'
        })

    
def book_mark(request, google_books_id,book_slug):

    base_url = "https://www.googleapis.com/books/v1/volumes/"

    # Send a GET request to the Google Books API
    response = requests.get(base_url + str(google_books_id))

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response as JSON
        data = response.json()

        # Extract the book details from the data
        book_title = data['volumeInfo']['title']
        book_slug = slugify(book_title)

    if request.method == "POST":
        user_bookmark = get_object_or_404(UserBookmark, google_books_id=str(google_books_id))
        user = request.user

        status = request.POST.get('status')
        if not status:
            return JsonResponse({'error': 'Status not provided'}, status=400)

        user_bookmark.status = status
        user_bookmark.save()

        return JsonResponse({'message': 'Bookmark updated successfully'})

    # For GET requests, you might want to render a template or redirect without a context
    return redirect('book_detail', book_id=google_books_id, book_slug=book_slug)
