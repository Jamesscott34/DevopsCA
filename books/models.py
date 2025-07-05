"""
Database models for the Book Catalog application.

This module defines the data structures used to store user accounts and book information
in the database. It includes models for user authentication and book management.
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
    """
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Will store hashed password
    created_at = models.DateTimeField(auto_now_add=True)
    
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

class Book(models.Model):
    """
    Model for storing book information in the catalog.
    
    This model represents a book in the user's personal library. It includes
    basic book metadata like title, author, and publication details, plus
    tracking for whether the book has been read.
    
    Attributes:
        title (str): Book title (max 200 characters)
        author (str): Book author (max 100 characters)
        description (str): Optional book description/summary
        published_date (date): When the book was published
        isbn (str): International Standard Book Number (unique, optional)
        is_read (bool): Whether the user has read this book
    """
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    published_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True, blank=True, null=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        """Return the book title as the string representation."""
        return self.title
