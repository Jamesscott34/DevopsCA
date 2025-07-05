"""
Django forms for the Book Catalog application.

This module defines the form classes used for data input and validation.
Forms handle user registration, login, and book management with proper
validation and security measures.
"""

from django import forms
from django.contrib.auth.hashers import check_password
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

class PasswordChangeForm(forms.Form):
    """
    Form for changing user passwords.
    
    This form allows users to update their passwords with proper validation.
    It requires the current password for security and confirmation of the new password.
    
    Fields:
        current_password: Current password for verification
        new_password: New password to set
        confirm_new_password: Confirmation of new password
    """
    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Current Password'
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='New Password'
    )
    confirm_new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label='Confirm New Password'
    )
    
    def __init__(self, user, *args, **kwargs):
        """
        Initialize form with user instance for password validation.
        
        Args:
            user: User instance to validate current password against
            *args, **kwargs: Standard form arguments
        """
        self.user = user
        super().__init__(*args, **kwargs)
    
    def clean(self):
        """
        Custom validation for password change.
        
        This method validates that:
        1. Current password is correct
        2. New password and confirmation match
        3. New password is different from current password
        """
        cleaned_data = super().clean()
        current_password = cleaned_data.get('current_password')
        new_password = cleaned_data.get('new_password')
        confirm_new_password = cleaned_data.get('confirm_new_password')
        
        # Check if current password is correct
        if current_password and not check_password(current_password, self.user.password):
            raise forms.ValidationError("Current password is incorrect!")
        
        # Check if new passwords match
        if new_password and confirm_new_password and new_password != confirm_new_password:
            raise forms.ValidationError("New passwords do not match!")
        
        # Check if new password is different from current
        if current_password and new_password and current_password == new_password:
            raise forms.ValidationError("New password must be different from current password!")
        
        return cleaned_data

class ProfileEditForm(forms.ModelForm):
    """
    Form for editing user profile information.
    
    This form allows users to update their username and email address.
    It excludes the password field as password changes are handled separately.
    
    Fields:
        username: Username for login (can be updated)
        email: Email address for account recovery (can be updated)
    """
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
    
    def clean_username(self):
        """
        Validate username uniqueness excluding current user.
        
        This method ensures the username is unique while allowing users
        to keep their current username unchanged.
        """
        username = self.cleaned_data.get('username')
        if username and User.objects.filter(username=username).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("This username is already taken!")
        return username
    
    def clean_email(self):
        """
        Validate email uniqueness excluding current user.
        
        This method ensures the email is unique while allowing users
        to keep their current email unchanged.
        """
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("This email is already registered!")
        return email

