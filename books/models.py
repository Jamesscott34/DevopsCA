"""
Database models for the Book Catalog application.

This module defines the data structures used to store user accounts and book information
in the database. It includes models for user authentication, book management, and notifications.
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password

class User(models.Model):
    """
    Custom user model for storing user account information.
    
    This model handles user registration, authentication, and session management.
    Passwords are automatically hashed using Django's secure hashing algorithms
    before being stored in the database.
    
    Attributes:
        username (str): Unique username for login (max 100 characters)
        email (str): Unique email address for account recovery
        password (str): Hashed password (max 128 characters)
        created_at (datetime): Timestamp when account was created
        admin_referral (ForeignKey): Admin referral or notes for this user
        user_notes (str): User personal notes or referral info (max 255 characters)
    """
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Will store hashed password
    created_at = models.DateTimeField(auto_now_add=True)
    admin_referral = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True, blank=True, related_name='referred_users', help_text='Book selected by admin as a referral for this user.')
    user_notes = models.TextField(blank=True, null=True, help_text='User personal notes or referral info.')
    
    def save(self, *args, **kwargs):
        """
        Override save method to automatically hash passwords.
        
        This ensures that passwords are never stored in plain text. The hashing
        only occurs when creating a new user, not when updating existing users.
        """
        # Hash the password before saving
        if not self.pk:  # Only hash on creation, not update
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
    
    def __str__(self):
        """Return the username as the string representation of the user."""
        return self.username

    @property
    def is_authenticated(self):
        return True

class Tag(models.Model):
    """
    Model for book tags/categories.
    Allows users to assign multiple tags to books for better organization and filtering.
    Attributes:
        name (str): Name of the tag/category (unique)
    """
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    """
    Model for storing book information in the catalog.
    
    This model represents a book in the user's personal library. It includes
    basic book metadata like title, author, and publication details, plus
    tracking for whether the book has been read and how many times it's been viewed.
    
    Attributes:
        title (str): Book title (max 200 characters)
        author (str): Book author (max 100 characters)
        description (str): Optional book description/summary
        published_date (date): When the book was published
        isbn (str): International Standard Book Number (unique, optional)
        is_read (bool): Whether the user has read this book
        view_count (int): Number of times the book has been viewed
        added_by (User): User who added the book to the catalog
        cover_image (ImageField): Optional cover image for the book
        tags (ManyToManyField): Tags/categories for this book
    """
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    published_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    view_count = models.IntegerField(default=0)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='added_books')
    cover_image = models.ImageField(
        upload_to='book_covers/',
        blank=True,
        null=True,
        help_text='Optional cover image for the book.'
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name='books', help_text='Tags/categories for this book.')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return the book title as the string representation."""
        return self.title
    
    def increment_view_count(self):
        """Increment the view count for this book."""
        self.view_count += 1
        self.save(update_fields=['view_count'])
    
    @classmethod
    def get_most_read(cls):
        """Get the most read books."""
        return cls.objects.filter(is_read=True).order_by('-view_count')[:5]
    
    @classmethod
    def get_most_viewed(cls):
        """Get the most viewed books."""
        return cls.objects.order_by('-view_count')[:5]

class Notification(models.Model):
    """
    Model for storing user notifications and book recommendations.
    
    This model handles notifications sent by admins to users, including
    book recommendations and other important messages. Notifications can
    be marked as read and are associated with specific users.
    
    Attributes:
        user (User): The user who receives the notification
        title (str): Notification title/headline
        message (str): Detailed notification message
        book_recommendation (Book): Optional book being recommended
        is_read (bool): Whether the user has read the notification
        created_at (datetime): When the notification was created
        notification_type (str): Type of notification (recommendation, general, etc.)
    """
    NOTIFICATION_TYPES = [
        ('recommendation', 'Book Recommendation'),
        ('general', 'General Message'),
        ('system', 'System Notification'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    book_recommendation = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, blank=True, related_name='notifications')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='general')
    
    class Meta:
        """Meta options for ordering notifications by creation date."""
        ordering = ['-created_at']
    
    def __str__(self):
        """Return a string representation of the notification."""
        return f"Notification for {self.user.username}: {self.title}"
    
    def mark_as_read(self):
        """Mark the notification as read."""
        self.is_read = True
        self.save()
