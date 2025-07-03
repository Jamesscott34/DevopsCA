from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
       
        fields = ['title', 'author', 'published_date', 'is_read']
        widgets = {
            'published_date': forms.DateInput(attrs={'type': 'date'}),
        }
