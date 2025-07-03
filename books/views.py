from django.shortcuts import render, redirect, get_object_or_404
from .models import Book
from .forms import BookForm
from django.views.decorators.csrf import csrf_exempt
import requests
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Book
from .forms import BookForm
from datetime import datetime
import random


def home(request):
    books = Book.objects.all()
    return render(request, 'books/home.html', {'books': books})

def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = BookForm()
    return render(request, 'books/add_book.html', {'form': form})

def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = BookForm(instance=book)
    return render(request, 'books/edit_book.html', {'form': form})

def delete_book_by_isbn(request, isbn):
    book = get_object_or_404(Book, isbn=isbn)
    book.delete()
    return redirect('home')


def toggle_read_status(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.is_read = not book.is_read
    book.save()
    return redirect('home')

def read_books(request):
    books = Book.objects.filter(is_read=True)
    return render(request, 'books/read_books.html', {'books': books})

def unread_books(request):
    books = Book.objects.filter(is_read=False)
    return render(request, 'books/unread_books.html', {'books': books})

import requests
from django.shortcuts import render

@csrf_exempt
def open_library_search(request):
    query = request.GET.get('query', '')
    results = []

    if query:
        # If user searched, use the search endpoint
        response = requests.get('https://openlibrary.org/search.json', params={'q': query})
        if response.status_code == 200:
            data = response.json()
            docs = data.get('docs', [])[:30]
            for book in docs:
                results.append({
                    'title': book.get('title', 'No Title'),
                    'author': ', '.join(book.get('author_name', ['Unknown'])),
                    'publish_year': book.get('first_publish_year', 'Unknown'),
                    'isbn': book.get('isbn', [''])[0] if book.get('isbn') else '',
                    'cover_url': f"https://covers.openlibrary.org/b/isbn/{book['isbn'][0]}-L.jpg" if book.get('isbn') else '',
                })
    else:
        # Default list: use a subject and sort alphabetically
        subject = 'fiction'  # You can change this
        response = requests.get(f'https://openlibrary.org/subjects/{subject}.json?limit=30')
        if response.status_code == 200:
            data = response.json()
            works = sorted(data.get('works', []), key=lambda x: x.get('title', '').lower())
            for book in works:
                results.append({
                    'title': book.get('title', 'No Title'),
                    'author': ', '.join([a.get('name', 'Unknown') for a in book.get('authors', [])]),
                    'publish_year': book.get('first_publish_year', 'Unknown'),
                    'isbn': '',  # Subject API doesn’t return ISBN
                    'cover_url': f"https://covers.openlibrary.org/b/id/{book['cover_id']}-L.jpg" if book.get('cover_id') else '',
                })

    return render(request, 'books/open_library.html', {
        'results': results,
        'query': query
    })

def toggle_read(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    book.is_read = not book.is_read
    book.save()
    return redirect('home')



def save_open_library_book(request):
    if request.method == "POST":
        title = request.POST.get("title")
        author = request.POST.get("author")
        raw_date = request.POST.get("published_date")
        isbn = request.POST.get("isbn", "").strip()

        # Convert "1976" → "1976-01-01"
        try:
            if raw_date and len(raw_date) == 4:
                published_date = datetime.strptime(raw_date + "-01-01", "%Y-%m-%d").date()
            else:
                published_date = datetime.strptime(raw_date, "%Y-%m-%d").date()
        except Exception:
            published_date = None  # optional: fallback or raise

        # Auto-generate unique ISBN if not provided or invalid
        if not isbn or isbn.lower().startswith("js"):
            from .models import Book
            existing_isbns = Book.objects.values_list("isbn", flat=True)
            while True:
                new_isbn = f"JS{random.randint(1000000, 9999999)}"
                if new_isbn not in existing_isbns:
                    isbn = new_isbn
                    break

        Book.objects.create(
            title=title,
            author=author,
            published_date=published_date,
            isbn=isbn,
            description=request.POST.get("description", ""),  # optional
        )
        return redirect("home")


def generate_js_isbn():
    count = Book.objects.count() + 1
    return f"JS{count:05d}"  # e.g. JS00001
