"""
Django views for the Book Catalog application.

This module contains all the view functions that handle HTTP requests and responses.
Views manage user authentication, book operations, and external API integration.
Each view function processes specific URLs and returns appropriate responses.
"""

from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, User, Notification
from .forms import BookForm, UserRegistrationForm, LoginForm, PasswordChangeForm, ProfileEditForm, NotificationForm, BulkNotificationForm, AdminEmailChangeForm
from django.views.decorators.csrf import csrf_exempt
import requests
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Book
from .forms import BookForm
from datetime import datetime
import random
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password

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
    print(f"DEBUG: get_current_user called. Session keys: {list(request.session.keys())}")
    
    if 'user_id' in request.session:
        try:
            user_id = request.session['user_id']
            print(f"DEBUG: Found user_id in session: {user_id}")
            current_user = User.objects.get(id=user_id)
            print(f"DEBUG: Retrieved user: {current_user.username}")
        except User.DoesNotExist:
            print(f"DEBUG: User with id {user_id} not found in database")
            pass
    else:
        print("DEBUG: No user_id found in session")
    
    return current_user

def home(request):
    """
    Display the main homepage with all books in the catalog, with search and filter options.
    
    This view shows the primary interface where users can see all their books
    in a table format. It includes action buttons for adding books and filtering
    by read/unread status. The view also displays a personalized welcome message
    for logged-in users and tracks book views for statistics.
    Users must be logged in to access this page.
    Now supports filtering by search query (title, author, ISBN) and read status.
    
    Args:
        request: Django HttpRequest object
        
    Returns:
        Rendered home.html template with books data and user context
    """
    current_user = get_current_user(request)
    
    # Require authentication
    if not current_user:
        messages.error(request, 'You must be logged in to access the book catalog.')
        return redirect('login_user')
    
    # Get search and filter parameters
    search_query = request.GET.get('search', '').strip()
    read_status = request.GET.get('read_status', '')

    books = Book.objects.all()
    if search_query:
        books = books.filter(
            title__icontains=search_query
        ) | books.filter(
            author__icontains=search_query
        ) | books.filter(
            isbn__icontains=search_query
        )
    if read_status == 'read':
        books = books.filter(is_read=True)
    elif read_status == 'unread':
        books = books.filter(is_read=False)
    
    # Track book views for statistics (increment view count for each book)
    for book in books:
        book.increment_view_count()
    
    return render(request, 'books/home.html', {
        'books': books,
        'current_user': current_user,
        'search_query': search_query,
        'read_status': read_status,
    })

def add_book(request):
    """
    Handle adding new books to the catalog with improved validation and error handling.

    This view provides a form for users to manually enter book information.
    It handles both GET requests (display form) and POST requests (save book).
    After successful book creation, users are redirected to the home page.
    The view tracks which user added the book for statistics.
    Now handles validation and user-friendly error messages.

    Args:
        request: Django HttpRequest object
    Returns:
        Rendered add_book.html template or redirect to home page
    """
    current_user = get_current_user(request)
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            try:
                book = form.save(commit=False)
                book.added_by = current_user
                # Check for duplicate ISBN if provided
                if book.isbn and Book.objects.filter(isbn=book.isbn).exists():
                    form.add_error('isbn', 'A book with this ISBN already exists.')
                else:
                    book.save()
                    messages.success(request, 'Book added successfully!')
                    return redirect('home')
            except Exception as e:
                form.add_error(None, f'An unexpected error occurred: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BookForm()
    return render(request, 'books/add_book.html', {'form': form, 'current_user': current_user})

def edit_book(request, pk):
    """
    Handle editing existing books in the catalog with improved validation and error handling.

    This view allows users to modify book information. It pre-populates the
    form with existing book data and saves changes when submitted. The view
    uses the book's primary key to identify which book to edit.
    Now includes robust validation and user-friendly error messages.

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
            try:
                updated_book = form.save(commit=False)
                # Check for duplicate ISBN if changed
                if updated_book.isbn and Book.objects.filter(isbn=updated_book.isbn).exclude(pk=book.pk).exists():
                    form.add_error('isbn', 'A book with this ISBN already exists.')
                else:
                    updated_book.save()
                    messages.success(request, 'Book updated successfully!')
                    return redirect('home')
            except Exception as e:
                form.add_error(None, f'An unexpected error occurred: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
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
    for admin users vs regular users. All users go to the home page after login.
    If a user is already logged in, they are redirected to the appropriate page.
    
    Args:
        request: Django HttpRequest object
        
    Returns:
        Rendered login.html template or redirect based on user type
    """
    current_user = get_current_user(request)
    
    # If user is already logged in, redirect them to appropriate page
    if current_user:
        if current_user.username == 'admin':
            messages.info(request, 'You are already logged in as admin.')
            return redirect('admin_dashboard')
        else:
            messages.info(request, f'You are already logged in as {current_user.username}.')
            return redirect('home')
    
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
    
    This view provides admins with an overview of the system including user counts,
    book statistics, and quick access to administrative functions. It also includes
    notification statistics for the notification management section.
    
    Args:
        request: Django HttpRequest object
        
    Returns:
        Rendered admin_dashboard.html template with system statistics
    """
    current_user = get_current_user(request)
    if not current_user or current_user.username != 'admin':
        messages.error(request, 'You must be admin to access the admin dashboard.')
        return redirect('login_user')
    
    # Get system statistics
    total_users = User.objects.count()
    total_books = Book.objects.count()
    read_books = Book.objects.filter(is_read=True).count()
    unread_books = Book.objects.filter(is_read=False).count()
    all_users = User.objects.all().order_by('created_at')
    
    # Calculate reading progress percentage
    if total_books > 0:
        read_percentage = (read_books / total_books) * 100
        unread_percentage = (unread_books / total_books) * 100
    else:
        read_percentage = 0
        unread_percentage = 0
    
    # Get notification statistics
    total_notifications = Notification.objects.count()
    read_notifications = Notification.objects.filter(is_read=True).count()
    unread_notifications = Notification.objects.filter(is_read=False).count()
    
    # Get notification type counts
    recommendation_count = Notification.objects.filter(notification_type='recommendation').count()
    general_count = Notification.objects.filter(notification_type='general').count()
    system_count = Notification.objects.filter(notification_type='system').count()
    
    # Get most read and most viewed books
    most_read_books = Book.get_most_read()
    most_viewed_books = Book.get_most_viewed()
    
    context = {
        'current_user': current_user,
        'total_users': total_users,
        'total_books': total_books,
        'read_books': read_books,
        'unread_books': unread_books,
        'read_percentage': read_percentage,
        'unread_percentage': unread_percentage,
        'all_users': all_users,
        'total_notifications': total_notifications,
        'read_notifications': read_notifications,
        'unread_notifications': unread_notifications,
        'recommendation_count': recommendation_count,
        'general_count': general_count,
        'system_count': system_count,
        'most_read_books': most_read_books,
        'most_viewed_books': most_viewed_books,
    }
    
    return render(request, 'books/admin_dashboard.html', context)

def delete_user(request, user_id):
    """
    Delete a user from the system (admin only).
    
    This view allows admin users to delete other user accounts from the system.
    It prevents the admin from deleting themselves and provides confirmation
    messages for successful or failed deletions.
    
    Args:
        request: Django HttpRequest object
        user_id: ID of the user to delete
        
    Returns:
        Redirect to admin dashboard with success/error message
    """
    current_user = get_current_user(request)
    
    # Check if current user is admin
    if not current_user or current_user.username != 'admin':
        messages.error(request, 'You must be admin to perform this action.')
        return redirect('login_user')
    
    try:
        user_to_delete = User.objects.get(id=user_id)
        
        # Prevent admin from deleting themselves
        if user_to_delete.username == 'admin':
            messages.error(request, 'You cannot delete the admin user.')
            return redirect('admin_dashboard')
        
        # Delete the user
        username = user_to_delete.username
        user_to_delete.delete()
        messages.success(request, f'User "{username}" has been deleted successfully.')
        
    except User.DoesNotExist:
        messages.error(request, 'User not found.')
    except Exception as e:
        messages.error(request, f'Error deleting user: {str(e)}')
    
    return redirect('admin_dashboard')

def change_password(request):
    """
    Handle password change for a user.
    
    This view allows users to change their password. It processes the form data,
    validates the current password, and updates the user's password in the database.
    
    Args:
        request: Django HttpRequest object
        
    Returns:
        Rendered change_password.html template or redirect to home page
    """
    current_user = get_current_user(request)
    if not current_user:
        messages.error(request, 'You must be logged in to change your password.')
        return redirect('login_user')
    
    if request.method == 'POST':
        form = PasswordChangeForm(current_user, request.POST)
        if form.is_valid():
            user = User.objects.get(id=current_user.id)
            user.password = make_password(form.cleaned_data['new_password'])
            user.save()
            messages.success(request, 'Your password has been changed successfully.')
            return redirect('home')
    else:
        form = PasswordChangeForm(current_user)
    
    return render(request, 'books/change_password.html', {'form': form, 'current_user': current_user})

def edit_profile(request):
    """
    Handle profile editing for a user.
    
    This view allows users to modify their profile information. It processes the form data,
    updates the user's profile in the database, and provides a confirmation message.
    
    Args:
        request: Django HttpRequest object
        
    Returns:
        Rendered edit_profile.html template or redirect to home page
    """
    current_user = get_current_user(request)
    if not current_user:
        messages.error(request, 'You must be logged in to edit your profile.')
        return redirect('login_user')
    
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=current_user)
        if form.is_valid():
            form.save()
            # Update session with new username if changed
            if 'user_id' in request.session:
                updated_user = User.objects.get(id=current_user.id)
                request.session['user_id'] = updated_user.id
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('home')
    else:
        form = ProfileEditForm(instance=current_user)
    
    return render(request, 'books/edit_profile.html', {'form': form, 'current_user': current_user})

def delete_profile(request):
    """
    Handle profile deletion for a user.
    
    This view allows users to delete their profile from the system. It provides a confirmation
    message and redirects to the login page after the profile is deleted.
    
    Args:
        request: Django HttpRequest object
        
    Returns:
        Redirect to login page with logout message
    """
    current_user = get_current_user(request)
    if not current_user:
        messages.error(request, 'You must be logged in to delete your profile.')
        return redirect('login_user')
    
    # Prevent admin from deleting themselves
    if current_user.username == 'admin':
        messages.error(request, 'Admin users cannot delete their profile.')
        return redirect('home')
    
    if request.method == 'POST':
        username = current_user.username
        current_user.delete()
        request.session.flush()
        messages.success(request, f'Profile for user "{username}" has been deleted successfully.')
        return redirect('login_user')
    
    return render(request, 'books/delete_profile.html', {'current_user': current_user})

def send_notification(request, user_id=None):
    """
    Handle sending notifications to users (admin only).
    
    This view allows admins to send notifications to specific users or all users.
    It supports both individual notifications and bulk notifications with email options.
    Admin cannot send notifications to themselves.
    
    Args:
        request: Django HttpRequest object
        user_id: Optional user ID to send notification to specific user
        
    Returns:
        Rendered send_notification.html template or redirect to admin dashboard
    """
    current_user = get_current_user(request)
    if not current_user or current_user.username != 'admin':
        messages.error(request, 'You must be admin to send notifications.')
        return redirect('login_user')
    
    # Get target user if specified
    target_user = None
    if user_id:
        try:
            target_user = User.objects.get(id=user_id)
            # Admin cannot send notifications to themselves
            if target_user.username == 'admin':
                messages.error(request, 'Admin cannot send notifications to themselves.')
                return redirect('admin_dashboard')
        except User.DoesNotExist:
            messages.error(request, 'Target user not found.')
            return redirect('admin_dashboard')
    
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            notification_data = form.cleaned_data
            send_email = notification_data.pop('send_email', False)
            
            # Determine target users
            if target_user:
                # Send to specific user
                users_to_notify = [target_user]
            else:
                # Send to all regular users (exclude admin)
                users_to_notify = User.objects.exclude(username='admin')
            
            # Create notifications for each user
            notifications_created = 0
            for user in users_to_notify:
                notification = Notification.objects.create(
                    user=user,
                    title=notification_data['title'],
                    message=notification_data['message'],
                    notification_type=notification_data['notification_type'],
                    book_recommendation=notification_data.get('book_recommendation')
                )
                notifications_created += 1
                
                # Save book to user's reading list if requested
                if notification_data.get('save_book_to_list') and notification_data.get('book_recommendation'):
                    book = notification_data['book_recommendation']
                    # Check if user already has this book
                    if not Book.objects.filter(title=book.title, author=book.author, added_by=user).exists():
                        # Create a copy of the book for the user
                        new_book = Book.objects.create(
                            title=book.title,
                            author=book.author,
                            description=book.description,
                            published_date=book.published_date,
                            isbn=book.isbn,
                            is_read=False,  # Start as unread
                            added_by=user
                        )
                
                # TODO: Send email notification if requested
                if send_email:
                    # Email functionality would be implemented here
                    # Include book details and additional content in email
                    pass
            
            messages.success(request, f'Notification sent to {notifications_created} user(s) successfully.')
            return redirect('admin_dashboard')
    else:
        form = NotificationForm()
    
    return render(request, 'books/send_notification.html', {
        'form': form, 
        'current_user': current_user,
        'target_user': target_user
    })

def send_bulk_notification(request):
    """
    Handle sending bulk notifications to multiple users (admin only).
    
    This view allows admins to send the same notification to multiple users
    simultaneously with options for targeting specific user groups.
    Admin cannot send notifications to themselves.
    
    Args:
        request: Django HttpRequest object
        
    Returns:
        Rendered send_bulk_notification.html template or redirect to admin dashboard
    """
    current_user = get_current_user(request)
    if not current_user or current_user.username != 'admin':
        messages.error(request, 'You must be admin to send bulk notifications.')
        return redirect('login_user')
    
    if request.method == 'POST':
        form = BulkNotificationForm(request.POST)
        if form.is_valid():
            notification_data = form.cleaned_data
            send_email = notification_data.pop('send_email', False)
            
            # Determine target users based on selection
            target_users = notification_data['target_users']
            if target_users == 'all':
                users_to_notify = User.objects.exclude(username='admin')
            elif target_users == 'regular':
                users_to_notify = User.objects.exclude(username='admin')
            else:  # specific
                users_to_notify = notification_data['specific_users'].exclude(username='admin')
            
            # Create notifications for each user
            notifications_created = 0
            for user in users_to_notify:
                notification = Notification.objects.create(
                    user=user,
                    title=notification_data['title'],
                    message=notification_data['message'],
                    notification_type=notification_data['notification_type'],
                    book_recommendation=notification_data.get('book_recommendation')
                )
                notifications_created += 1
                
                # Save book to user's reading list if requested
                if notification_data.get('save_book_to_list') and notification_data.get('book_recommendation'):
                    book = notification_data['book_recommendation']
                    # Check if user already has this book
                    if not Book.objects.filter(title=book.title, author=book.author, added_by=user).exists():
                        # Create a copy of the book for the user
                        new_book = Book.objects.create(
                            title=book.title,
                            author=book.author,
                            description=book.description,
                            published_date=book.published_date,
                            isbn=book.isbn,
                            is_read=False,  # Start as unread
                            added_by=user
                        )
                
                # TODO: Send email notification if requested
                if send_email:
                    # Email functionality would be implemented here
                    # Include book details and additional content in email
                    pass
            
            messages.success(request, f'Bulk notification sent to {notifications_created} user(s) successfully.')
            return redirect('admin_dashboard')
    else:
        form = BulkNotificationForm()
    
    return render(request, 'books/send_bulk_notification.html', {
        'form': form, 
        'current_user': current_user
    })

def view_notifications(request):
    """
    Display notifications for the current user.
    
    This view shows all notifications for the logged-in user, including
    book recommendations and general messages. Users can mark notifications as read.
    
    Args:
        request: Django HttpRequest object
        
    Returns:
        Rendered view_notifications.html template with user's notifications
    """
    current_user = get_current_user(request)
    print(f"DEBUG: view_notifications called. Current user: {current_user}")
    
    if not current_user:
        print("DEBUG: No current user found, redirecting to login")
        messages.error(request, 'You must be logged in to view notifications.')
        return redirect('login_user')
    
    print(f"DEBUG: User authenticated: {current_user.username}")
    
    notifications = Notification.objects.filter(user=current_user).order_by('-created_at')
    unread_count = notifications.filter(is_read=False).count()
    
    print(f"DEBUG: Found {notifications.count()} notifications, {unread_count} unread")
    
    return render(request, 'books/view_notifications.html', {
        'notifications': notifications, 
        'current_user': current_user,
        'unread_count': unread_count
    })

def mark_notification_read(request, notification_id):
    """
    Mark a notification as read for the current user.
    
    This view allows users to mark individual notifications as read.
    It validates that the user owns the notification before updating.
    
    Args:
        request: Django HttpRequest object
        notification_id: ID of the notification to mark as read
        
    Returns:
        Redirect to notifications page with success message
    """
    current_user = get_current_user(request)
    if not current_user:
        messages.error(request, 'You must be logged in to mark notifications as read.')
        return redirect('login_user')
    
    try:
        notification = Notification.objects.get(id=notification_id, user=current_user)
        notification.mark_as_read()
        messages.success(request, 'Notification marked as read.')
    except Notification.DoesNotExist:
        messages.error(request, 'Notification not found.')
    
    return redirect('view_notifications')

def mark_all_notifications_read(request):
    """
    Mark all notifications as read for the current user.
    
    This view allows users to mark all their unread notifications as read
    in one action for convenience.
    
    Args:
        request: Django HttpRequest object
        
    Returns:
        Redirect to notifications page with success message
    """
    current_user = get_current_user(request)
    if not current_user:
        messages.error(request, 'You must be logged in to mark notifications as read.')
        return redirect('login_user')
    
    unread_notifications = Notification.objects.filter(user=current_user, is_read=False)
    count = unread_notifications.count()
    unread_notifications.update(is_read=True)
    
    messages.success(request, f'{count} notification(s) marked as read.')
    return redirect('view_notifications')

def change_user_email(request, user_id):
    """
    Handle changing a user's email address (admin only).
    
    This view allows admins to change email addresses for any user in the system.
    It includes proper validation and confirmation to ensure data integrity.
    Admin can only change their own email address, not other users'.
    
    Args:
        request: Django HttpRequest object
        user_id: ID of the user whose email will be changed
        
    Returns:
        Rendered change_user_email.html template or redirect to admin dashboard
    """
    current_user = get_current_user(request)
    if not current_user or current_user.username != 'admin':
        messages.error(request, 'You must be admin to change user emails.')
        return redirect('login_user')
    
    try:
        target_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('admin_dashboard')
    
    # Admin can only change their own email address
    if target_user.username != 'admin':
        messages.error(request, 'Admin can only change their own email address.')
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        form = AdminEmailChangeForm(target_user, request.POST)
        if form.is_valid():
            new_email = form.cleaned_data['new_email']
            target_user.email = new_email
            target_user.save()
            messages.success(request, f'Email for user "{target_user.username}" has been updated to {new_email}.')
            return redirect('admin_dashboard')
    else:
        form = AdminEmailChangeForm(target_user)
    
    return render(request, 'books/change_user_email.html', {
        'form': form,
        'current_user': current_user,
        'target_user': target_user
    })
