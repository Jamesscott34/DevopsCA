from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_book, name='add_book'),
    path('edit/<int:book_id>/', views.edit_book, name='edit_book'),
    path('delete/<str:isbn>/', views.delete_book_by_isbn, name='delete_book_by_isbn'),
    path('toggle/<int:book_id>/', views.toggle_read, name='toggle_read'),
    path('read/', views.read_books, name='read_books'),
    path('unread/', views.unread_books, name='unread_books'),
    path('open-library/', views.open_library_search, name='open_library_search'), 
    path('open-library/save/', views.save_open_library_book, name='save_open_library_book'),
]