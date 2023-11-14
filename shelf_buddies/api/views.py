from django.shortcuts import render, get_object_or_404, HttpResponse
from django.views import View
from django.conf import settings
from .models import Books, User_Bookmark
import requests

# Create your views here.

class BookDetailView(View):
    def get(self, request, *args, **kwargs):
        book_id = kwargs.get('id')
        book = Books.objects.filter(google_books_id=book_id).first()

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
        }
        return render(request, 'book_detail2.html', context)
    
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