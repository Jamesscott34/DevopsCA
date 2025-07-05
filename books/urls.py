"""
URL configuration for the Book Catalog application.

This module defines all the URL patterns for the application, including
book management, user authentication, profile management, and admin functions.
Each URL pattern maps to a specific view function that handles the request.
"""

from django.urls import path
from . import views

# URL patterns for the Book Catalog application
urlpatterns = [
    # Main application pages
    path('', views.home, name='home'),  # Home page with book catalog
    
    # User authentication and registration
    path('register/', views.register_user, name='register_user'),  # User registration
    path('login/', views.login_user, name='login_user'),  # User login
    path('logout/', views.logout_user, name='logout_user'),  # User logout
    
    # Admin functionality
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),  # Admin dashboard
    path('admin-dashboard/delete-user/<int:user_id>/', views.delete_user, name='delete_user'),  # Delete user (admin only)
    
    # User profile management
    path('profile/edit/', views.edit_profile, name='edit_profile'),  # Edit user profile
    path('profile/change-password/', views.change_password, name='change_password'),  # Change password
    path('profile/delete/', views.delete_profile, name='delete_profile'),  # Delete user profile
    
    # Book management
    path('add/', views.add_book, name='add_book'),  # Add new book
    path('edit/<int:book_id>/', views.edit_book, name='edit_book'),  # Edit existing book
    path('delete/<str:isbn>/', views.delete_book_by_isbn, name='delete_book_by_isbn'),  # Delete book by ISBN
    path('toggle/<int:book_id>/', views.toggle_read, name='toggle_read'),  # Toggle read status
    
    # Book filtering and views
    path('read/', views.read_books, name='read_books'),  # Show only read books
    path('unread/', views.unread_books, name='unread_books'),  # Show only unread books
    
    # Open Library integration
    path('open-library/', views.open_library_search, name='open_library_search'),  # Search Open Library
    path('open-library/save/', views.save_open_library_book, name='save_open_library_book'),  # Save book from Open Library
]