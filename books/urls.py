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
    # Default redirect to login page
    path('', views.login_user, name='default'),  # Redirect root to login
    
    # User authentication and registration
    path('register/', views.register_user, name='register_user'),  # User registration
    path('login/', views.login_user, name='login_user'),  # User login
    path('logout/', views.logout_user, name='logout_user'),  # User logout
    
    # Admin functionality
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),  # Admin dashboard
    path('admin-dashboard/delete-user/<int:user_id>/', views.delete_user, name='delete_user'),  # Delete user (admin only)
    path('admin-dashboard/change-email/<int:user_id>/', views.change_user_email, name='change_user_email'),  # Change user email (admin only)
    path('admin-dashboard/edit-referral/<int:user_id>/', views.edit_admin_referral, name='edit_admin_referral'),  # Edit admin referral for user
    path('admin-dashboard/view-books/<int:user_id>/', views.admin_view_user_books, name='admin_view_user_books'),  # Admin view: books for user
    path('admin-dashboard/set-referral/<int:user_id>/', views.admin_set_referral, name='admin_set_referral'),  # Admin set referral book for user
    
    # User profile management
    path('profile/edit/', views.edit_profile, name='edit_profile'),  # Edit user profile
    path('profile/change-password/', views.change_password, name='change_password'),  # Change password
    path('profile/delete/', views.delete_profile, name='delete_profile'),  # Delete user profile
    
    # Notification system (updated URLs to avoid admin conflicts)
    path('notifications/', views.view_notifications, name='view_notifications'),  # View user notifications
    path('notifications/mark-read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),  # Mark notification as read
    path('notifications/mark-all-read/', views.mark_all_notifications_read, name='mark_all_notifications_read'),  # Mark all notifications as read
    path('send-notification/', views.send_notification, name='send_notification'),  # Send notification (admin)
    path('send-notification/<int:user_id>/', views.send_notification, name='send_notification_user'),  # Send notification to specific user
    path('send-bulk-notification/', views.send_bulk_notification, name='send_bulk_notification'),  # Send bulk notification (admin)
    
    # Book management
    path('home/', views.home, name='home'),  # Home page with book catalog (moved from root)
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