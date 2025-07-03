from django.shortcuts import render, redirect, get_object_or_404
from .models import Book
from .forms import BookForm

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

def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        return redirect('home')
    return render(request, 'books/confirm_delete.html', {'book': book})

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
