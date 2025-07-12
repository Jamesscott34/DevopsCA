"""
Django forms for the Book Catalog application.

This module defines the form classes used for data input and validation.
Forms handle user registration, login, book management, and notifications with proper
validation and security measures.
"""

from django import forms
from django.contrib.auth.hashers import check_password
from .models import Book, User, Notification, Tag

# forms.py

class BookForm(forms.ModelForm):
    """
    Form for adding and editing books in the catalog, now with tag selection.
    Users can assign multiple tags/categories to a book for better organization and filtering.
    
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
        cover_image: Optional image upload for book cover
        tags: Multiple tags/categories for the book
    """
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        help_text='Select one or more tags/categories for this book.'
    )

    class Meta:
        model = Book
        fields = ['title', 'author', 'published_date', 'isbn', 'description', 'is_read', 'cover_image', 'tags']
        widgets = {
            'published_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
            'is_read': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_isbn(self):
        isbn = self.cleaned_data.get('isbn')
        if not isbn or str(isbn).strip().lower() == 'none':
            return None
        return isbn

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

class AdminEmailChangeForm(forms.Form):
    """
    Form for admin to change user email addresses.
    
    This form allows admins to update email addresses for any user in the system.
    It includes validation to ensure the new email is unique and properly formatted.
    
    Fields:
        new_email: New email address for the user
        confirm_email: Confirmation of the new email address
    """
    new_email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter new email address'}),
        label='New Email Address'
    )
    confirm_email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Confirm new email address'}),
        label='Confirm Email Address'
    )
    
    def __init__(self, user, *args, **kwargs):
        """
        Initialize form with user instance for validation.
        
        Args:
            user: User instance whose email will be changed
            *args, **kwargs: Standard form arguments
        """
        self.user = user
        super().__init__(*args, **kwargs)
    
    def clean(self):
        """
        Custom validation for email change.
        
        This method validates that:
        1. New email and confirmation match
        2. New email is different from current email
        3. New email is unique in the system
        """
        cleaned_data = super().clean()
        new_email = cleaned_data.get('new_email')
        confirm_email = cleaned_data.get('confirm_email')
        
        # Check if emails match
        if new_email and confirm_email and new_email != confirm_email:
            raise forms.ValidationError("Email addresses do not match!")
        
        # Check if new email is different from current
        if new_email and new_email == self.user.email:
            raise forms.ValidationError("New email must be different from current email!")
        
        # Check if new email is unique
        if new_email and User.objects.filter(email=new_email).exclude(id=self.user.id).exists():
            raise forms.ValidationError("This email address is already registered by another user!")
        
        return cleaned_data

class NotificationForm(forms.ModelForm):
    """
    Form for creating and sending notifications to users.
    
    This form allows admins to create notifications that can be sent to users
    via email or displayed in their profile. It supports both general messages
    and book recommendations with options to save books to user lists.
    
    Fields:
        title: Notification title/headline
        message: Detailed notification message
        notification_type: Type of notification (recommendation, general, system)
        book_recommendation: Optional book to recommend
        send_email: Whether to send email notification
        save_book_to_list: Whether to save the book to user's reading list
        additional_email_content: Additional content for email notifications
    """
    send_email = forms.BooleanField(
        required=False,
        initial=True,
        label='Send Email Notification',
        help_text='Check this to send the notification via email as well'
    )
    save_book_to_list = forms.BooleanField(
        required=False,
        initial=False,
        label='Save Book to User Reading List',
        help_text='Automatically add the recommended book to user\'s reading list'
    )
    additional_email_content = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Additional content for email (optional)'}),
        label='Additional Email Content',
        help_text='Extra content to include in email notifications'
    )
    
    class Meta:
        model = Notification
        fields = ['title', 'message', 'notification_type', 'book_recommendation']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter notification title'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter notification message'}),
            'notification_type': forms.Select(attrs={'class': 'form-control'}),
            'book_recommendation': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        """Initialize form with available books for recommendations."""
        super().__init__(*args, **kwargs)
        # Only show books that exist in the catalog for recommendations
        self.fields['book_recommendation'].queryset = Book.objects.all().order_by('title')
        self.fields['book_recommendation'].required = False
        self.fields['book_recommendation'].empty_label = "No book recommendation"

class BulkNotificationForm(forms.Form):
    """
    Form for sending notifications to multiple users at once.
    
    This form allows admins to send the same notification to multiple users
    simultaneously, with options for targeting specific user groups and saving books.
    
    Fields:
        title: Notification title/headline
        message: Detailed notification message
        notification_type: Type of notification
        book_recommendation: Optional book to recommend
        target_users: Which users to send to (all, regular users, specific users)
        specific_users: List of specific users to target
        send_email: Whether to send email notifications
        save_book_to_list: Whether to save the book to user's reading list
        additional_email_content: Additional content for email notifications
    """
    title = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter notification title'})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter notification message'})
    )
    notification_type = forms.ChoiceField(
        choices=Notification.NOTIFICATION_TYPES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    book_recommendation = forms.ModelChoiceField(
        queryset=Book.objects.all().order_by('title'),
        required=False,
        empty_label="No book recommendation",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    TARGET_CHOICES = [
        ('all', 'All Users'),
        ('regular', 'Regular Users Only'),
        ('specific', 'Specific Users'),
    ]
    
    target_users = forms.ChoiceField(
        choices=TARGET_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text='Choose which users to send the notification to'
    )
    specific_users = forms.ModelMultipleChoiceField(
        queryset=User.objects.exclude(username='admin').order_by('username'),
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        help_text='Select specific users (admin cannot send notifications to themselves)'
    )
    send_email = forms.BooleanField(
        required=False,
        initial=True,
        label='Send Email Notifications',
        help_text='Check this to send email notifications to all targeted users'
    )
    save_book_to_list = forms.BooleanField(
        required=False,
        initial=False,
        label='Save Book to User Reading Lists',
        help_text='Automatically add the recommended book to all targeted users\' reading lists'
    )
    additional_email_content = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Additional content for email (optional)'}),
        label='Additional Email Content',
        help_text='Extra content to include in email notifications'
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['book_recommendation'].queryset = Book.objects.all().order_by('title')

    def clean(self):
        """Validate that specific users are selected when targeting specific users."""
        cleaned_data = super().clean()
        target_users = cleaned_data.get('target_users')
        specific_users = cleaned_data.get('specific_users')
        
        if target_users == 'specific' and not specific_users:
            raise forms.ValidationError("Please select at least one user when targeting specific users.")
        
        return cleaned_data

class AdminReferralForm(forms.ModelForm):
    """
    Form for editing the admin_referral field for a user (admin only).
    """
    admin_referral = forms.ModelChoiceField(
        queryset=Book.objects.all().order_by('title'),
        required=False,
        label='Referral Book',
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text='Select a book to refer to this user.'
    )
    class Meta:
        model = User
        fields = ['admin_referral']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['admin_referral'].queryset = Book.objects.all().order_by('title')

class AdminSetReferralForm(forms.ModelForm):
    """
    Form for admin to set a referral book for a user.
    """
    admin_referral = forms.ModelChoiceField(
        queryset=Book.objects.none(),  # Will be set in __init__
        required=False,
        label='Referral Book',
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text='Select a book to refer to this user.'
    )
    class Meta:
        model = User
        fields = ['admin_referral']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['admin_referral'].queryset = Book.objects.all().order_by('title')

