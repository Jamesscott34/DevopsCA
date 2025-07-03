from django.urls import path, include
from .views import (
    home, add_book, edit_book,
    delete_book, toggle_read_status,
    read_books, unread_books
)

urlpatterns = [
    path('', home, name='home'),
    path('add/', add_book, name='add_book'),
    path('edit/<int:pk>/', edit_book, name='edit_book'),
    path('delete/<int:pk>/', delete_book, name='delete_book'),
    path('toggle-read/<int:pk>/', toggle_read_status, name='toggle_read'),
    path('read/', read_books, name='read_books'),
    path('unread/', unread_books, name='unread_books'),
]
