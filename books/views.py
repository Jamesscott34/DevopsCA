"""
Django views for the Book Catalog application.

This module contains all the view functions that handle HTTP requests and responses.
Views manage user authentication, book operations, and external API integration.
Each view function processes specific URLs and returns appropriate responses.
"""

from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, User
from .forms import BookForm, UserRegistrationForm, LoginForm
from django.views.decorators.csrf import csrf_exempt
import requests
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Book
from .forms import BookForm
from datetime import datetime
import random
from django.contrib import messages
from django.contrib.auth.hashers import check_password

def get_current_user(request):
    """
    Helper function to retrieve the currently logged-in user from session.
    
    This function checks the session for a user_id and returns the corresponding
    User object. If no user is logged in or the session is invalid, it returns None.
    
    Args:
        request: Django HttpRequest object containing session data
        
    Returns:
        User object if logged in, None otherwise
    """
    current_user = None
    if 'user_id' in request.session:
        try:
            current_user = User.objects.get(id=request.session['user_id'])
        except User.DoesNotExist:
            pass
    return current_user

def home(request):
    """
    Display the main homepage with all books in the catalog.
    
    This view shows the primary interface where users can see all their books
    in a table format. It includes action buttons for adding books and filtering
    by read/unread status. The view also displays a personalized welcome message
    for logged-in users.
    
    Args:
        request: Django HttpRequest object
        
    Returns:
        Rendered home.html template with books data and user context
    """
    books = Book.objects.all()
    current_user = get_current_user(request)
    
    return render(request, 'books/home.html', {
        'books': books,
        'current_user': current_user
    })

def add_book(request):
    """
    Handle adding new books to the catalog.
    
    This view provides a form for users to manually enter book information.
    It handles both GET requests (display form) and POST requests (save book).
    After successful book creation, users are redirected to the home page.
    
    Args:
        request: Django HttpRequest object
        
    Returns:
        Rendered add_book.html template or redirect to home page
    """
    current_user = get_current_user(request)
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = BookForm()
    return render(request, 'books/add_book.html', {'form': form, 'current_user': current_user})

def edit_book(request, pk):
    """
    Handle editing existing books in the catalog.
    
    This view allows users to modify book information. It pre-populates the
    form with existing book data and saves changes when submitted. The view
    uses the book's primary key to identify which book to edit.
    
    Args:
        request: Django HttpRequest object
        pk: Primary key of the book to edit
        
    Returns:
        Rendered edit_book.html template or redirect to home page
    """
    current_user = get_current_user(request)
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = BookForm(instance=book)
    return render(request, 'books/edit_book.html', {'form': form, 'current_user': current_user})

def delete_book_by_isbn(request, isbn):
    """
    Delete a book from the catalog using its ISBN.
    
    This view removes a book from the database based on its ISBN number.
    It's used in the book table's delete action buttons. After deletion,
    users are redirected to the home page.
    
    Args:
        request: Django HttpRequest object
        isbn: ISBN of the book to delete
        
    Returns:
        Redirect to home page
    """
    book = get_object_or_404(Book, isbn=isbn)
    book.delete()
    return redirect('home')

def toggle_read_status(request, pk):
    """
    Toggle the read/unread status of a book.
    
    This view flips the is_read boolean field of a book. If the book was
    marked as read, it becomes unread, and vice versa. Used for quick
    status updates from the book table.
    
    Args:
        request: Django HttpRequest object
        pk: Primary key of the book to toggle
        
    Returns:
        Redirect to home page
    """
    book = get_object_or_404(Book, pk=pk)
    book.is_read = not book.is_read
    book.save()
    return redirect('home')

def read_books(request):
    """
    Display only books that have been marked as read.
    
    This view filters the book catalog to show only books where is_read=True.
    It provides a focused view for users who want to see their completed reading.
    
    Args:
        request: Django HttpRequest object
        
    Returns:
        Rendered read_books.html template with filtered books
    """
    current_user = get_current_user(request)
    books = Book.objects.filter(is_read=True)
    return render(request, 'books/read_books.html', {'books': books, 'current_user': current_user})

def unread_books(request):
    """
    Display only books that have not been read yet.
    
    This view filters the book catalog to show only books where is_read=False.
    It helps users focus on their reading list and books they still need to read.
    
    Args:
        request: Django HttpRequest object
        
    Returns:
        Rendered unread_books.html template with filtered books
    """
    current_user = get_current_user(request)
    books = Book.objects.filter(is_read=False)
    return render(request, 'books/unread_books.html', {'books': books, 'current_user': current_user})

import requests
from django.shortcuts import render

@csrf_exempt
def open_library_search(request):
    """
    Search and browse books from the Open Library API.
    
    This view integrates with the Open Library API to search for books and
    display results. Users can search by title/author or browse popular books.
    The view handles both search queries and default browsing functionality.
    
    Args:
        request: Django HttpRequest object with optional 'query' parameter
        
    Returns:
        Rendered open_library.html template with search results
    """
    current_user = get_current_user(request)
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
        subject = 'fiction'  
        response = requests.get(f'https://openlibrary.org/subjects/{subject}.json?limit=30')
        if response.status_code == 200:
            data = response.json()
            works = sorted(data.get('works', []), key=lambda x: x.get('title', '').lower())
            for book in works:
                results.append({
                    'title': book.get('title', 'No Title'),
                    'author': ', '.join([a.get('name', 'Unknown') for a in book.get('authors', [])]),
                    'publish_year': book.get('first_publish_year', 'Unknown'),
                    'isbn': '',  # Subject API doesn't return ISBN
                    'cover_url': f"https://covers.openlibrary.org/b/id/{book['cover_id']}-L.jpg" if book.get('cover_id') else '',
                })

    return render(request, 'books/open_library.html', {
        'results': results,
        'query': query,
        'current_user': current_user
    })

def toggle_read(request, book_id):
    """
    Toggle the read status of a book (alternative implementation).
    
    This is an alternative implementation of the read status toggle.
    It performs the same function as toggle_read_status but uses book_id
    instead of pk for consistency with URL patterns.
    
    Args:
        request: Django HttpRequest object
        book_id: ID of the book to toggle
        
    Returns:
        Redirect to home page
    """
    book = get_object_or_404(Book, pk=book_id)
    book.is_read = not book.is_read
    book.save()
    return redirect('home')

def save_open_library_book(request):
    """
    Save a book from Open Library search results to the local catalog.
    
    This view handles the process of importing books from the Open Library
    API into the user's personal catalog. It processes form data and creates
    new Book objects with auto-generated ISBNs if needed.
    
    Args:
        request: Django HttpRequest object with book data
        
    Returns:
        Redirect to home page after saving
    """
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
    """
    Generate a unique ISBN with 'JS' prefix for books without ISBNs.
    
    This function creates sequential ISBN numbers starting with 'JS' followed
    by a 5-digit number. It's used for books that don't have official ISBNs
    to ensure each book has a unique identifier.
    
    Returns:
        String containing the generated ISBN
    """
    count = Book.objects.count() + 1
    return f"JS{count:05d}"  # e.g. JS00001

def register_user(request):
    """
    Handle user registration and account creation.
    
    This view processes new user sign-ups. It validates the registration form,
    creates new User objects with hashed passwords, and sets up user sessions.
    After successful registration, users are automatically logged in.
    
    Args:
        request: Django HttpRequest object
        
    Returns:
        Rendered register_user.html template or redirect to home page
    """
    current_user = get_current_user(request)
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Store user ID in session
            request.session['user_id'] = user.id
            return redirect('home')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'books/register_user.html', {'form': form, 'current_user': current_user})

def login_user(request):
    """
    Handle user authentication and login.
    
    This view processes login attempts by validating username/password combinations
    against the database. It sets up user sessions and provides different redirects
    for admin users vs regular users. Admin users go to the admin dashboard.
    
    Args:
        request: Django HttpRequest object
        
    Returns:
        Rendered login.html template or redirect based on user type
    """
    current_user = get_current_user(request)
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print(f"DEBUG: Login attempt for username: {username}")
            try:
                user = User.objects.get(username=username)
                print(f"DEBUG: User found: {user.username}")
                if check_password(password, user.password):
                    print(f"DEBUG: Password correct for {user.username}")
                    request.session['user_id'] = user.id
                    if user.username == 'admin':
                        print(f"DEBUG: Redirecting admin to admin_dashboard")
                        messages.success(request, 'Welcome, Admin!')
                        return redirect('admin_dashboard')
                    else:
                        print(f"DEBUG: Redirecting regular user to home")
                        messages.success(request, f'Welcome, {user.username}!')
                        return redirect('home')
                else:
                    print(f"DEBUG: Password incorrect for {user.username}")
                    form.add_error(None, 'Invalid username or password.')
            except User.DoesNotExist:
                print(f"DEBUG: User {username} not found")
                form.add_error(None, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'books/login.html', {'form': form, 'current_user': current_user})

def logout_user(request):
    """
    Handle user logout and session cleanup.
    
    This view clears the user's session data and logs them out of the system.
    It displays a confirmation message and redirects to the login page.
    
    Args:
        request: Django HttpRequest object
        
    Returns:
        Redirect to login page with logout message
    """
    request.session.flush()
    messages.info(request, 'You have been logged out.')
    return redirect('login_user')

def admin_dashboard(request):
    """
    Display the admin dashboard with system statistics and management tools.
    
    This view provides a special interface for admin users with system-wide
    statistics, user management tools, and quick access to administrative
    functions. Only users with username 'admin' can access this dashboard.
    
    Args:
        request: Django HttpRequest object
        
    Returns:
        Rendered admin_dashboard.html template or redirect to login if not admin
    """
    current_user = get_current_user(request)
    print(f"DEBUG: admin_dashboard called, current_user: {current_user}")
    if not current_user or current_user.username != 'admin':
        print(f"DEBUG: Access denied to admin_dashboard")
        messages.error(request, 'You must be admin to view this page.')
        return redirect('login_user')
    
    print(f"DEBUG: Admin access granted, getting statistics")
    # Get some statistics for admin dashboard
    total_books = Book.objects.count()
    read_books = Book.objects.filter(is_read=True).count()
    unread_books = Book.objects.filter(is_read=False).count()
    total_users = User.objects.count()
    
    return render(request, 'books/admin_dashboard.html', {
        'current_user': current_user,
        'total_books': total_books,
        'read_books': read_books,
        'unread_books': unread_books,
        'total_users': total_users
    })
