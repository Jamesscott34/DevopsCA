"""
Django forms for the Book Catalog application.

This module defines the form classes used for data input and validation.
Forms handle user registration, login, and book management with proper
validation and security measures.
"""

from django import forms
from .models import Book, User

# forms.py

class BookForm(forms.ModelForm):
    """
    Form for adding and editing books in the catalog.
    
    This form provides a user-friendly interface for entering book information.
    It includes proper field validation and Bootstrap styling for the UI.
    The form handles both creating new books and updating existing ones.
    
    Fields:
        title: Book title with text input
        author: Book author with text input  
        published_date: Date picker for publication date
        isbn: Text input for ISBN (optional)
        description: Multi-line text area for book summary
        is_read: Checkbox to mark book as read/unread
    """
    class Meta:
        model = Book
        fields = ['title', 'author', 'published_date', 'isbn', 'description', 'is_read']
        widgets = {
            'published_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
            'is_read': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class UserRegistrationForm(forms.ModelForm):
    """
    Form for user registration and account creation.
    
    This form handles new user sign-ups with username, email, and password.
    It includes password confirmation to prevent typos and ensures data
    integrity through Django's built-in validation.
    
    Fields:
        username: Unique username for login
        email: Valid email address for account recovery
        password: Secure password field (hidden input)
        confirm_password: Password confirmation field
    """
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
    
    def clean(self):
        """
        Custom validation to ensure passwords match.
        
        This method checks that the password and confirm_password fields
        contain the same value. If they don't match, it raises a validation
        error to prevent account creation with mismatched passwords.
        """
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match!")
        
        return cleaned_data

class LoginForm(forms.Form):
    """
    Form for user authentication and login.
    
    This form provides a simple interface for users to log into their accounts.
    It includes username and password fields with proper validation and
    Bootstrap styling for consistent UI appearance.
    
    Fields:
        username: Username for login
        password: Password for authentication (hidden input)
    """
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

