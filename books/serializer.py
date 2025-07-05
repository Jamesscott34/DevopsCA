"""
Django REST Framework serializers for the Book Catalog API.

This module defines serializers for converting Django model instances to JSON
and vice versa for API communication. Each serializer handles data validation
and transformation for specific models.
"""

from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Book, User, Notification

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model with password handling.
    
    This serializer handles user data for API operations, including
    proper password hashing and field validation. Passwords are hashed
    when creating or updating users.
    """
    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'confirm_password', 'created_at']
        read_only_fields = ['id', 'created_at']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}
        }
    
    def validate(self, attrs):
        """
        Validate user data, ensuring passwords match and are provided when needed.
        
        Args:
            attrs: Dictionary of field values
            
        Returns:
            Validated attributes
            
        Raises:
            ValidationError: If passwords don't match or other validation fails
        """
        if self.instance is None:  # Creating new user
            if not attrs.get('password'):
                raise serializers.ValidationError("Password is required for new users.")
            if attrs.get('password') != attrs.get('confirm_password'):
                raise serializers.ValidationError("Passwords do not match.")
        else:  # Updating existing user
            if attrs.get('password') and attrs.get('password') != attrs.get('confirm_password'):
                raise serializers.ValidationError("Passwords do not match.")
        
        return attrs
    
    def create(self, validated_data):
        """
        Create a new user with hashed password.
        
        Args:
            validated_data: Validated user data
            
        Returns:
            Created User instance
        """
        validated_data.pop('confirm_password', None)
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        """
        Update user with hashed password if provided.
        
        Args:
            instance: Existing User instance
            validated_data: Validated user data
            
        Returns:
            Updated User instance
        """
        validated_data.pop('confirm_password', None)
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().update(instance, validated_data)

class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for Book model with enhanced field handling.
    
    This serializer handles book data for API operations, including
    proper field validation and user attribution.
    """
    added_by_username = serializers.CharField(source='added_by.username', read_only=True)
    is_read_display = serializers.CharField(source='get_is_read_display', read_only=True)
    
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author', 'description', 'published_date', 
            'isbn', 'is_read', 'view_count', 'added_by', 'added_by_username',
            'is_read_display', 'created_at'
        ]
        read_only_fields = ['id', 'view_count', 'added_by', 'created_at']
    
    def create(self, validated_data):
        """
        Create a new book with user attribution.
        
        Args:
            validated_data: Validated book data
            
        Returns:
            Created Book instance
        """
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['added_by'] = request.user
        return super().create(validated_data)

class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for Notification model with user and book details.
    
    This serializer handles notification data for API operations,
    including user and book recommendation details.
    """
    user_username = serializers.CharField(source='user.username', read_only=True)
    book_title = serializers.CharField(source='book_recommendation.title', read_only=True)
    book_author = serializers.CharField(source='book_recommendation.author', read_only=True)
    notification_type_display = serializers.CharField(source='get_notification_type_display', read_only=True)
    
    class Meta:
        model = Notification
        fields = [
            'id', 'user', 'user_username', 'title', 'message', 
            'notification_type', 'notification_type_display', 'book_recommendation',
            'book_title', 'book_author', 'is_read', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'created_at']
    
    def create(self, validated_data):
        """
        Create a new notification with user attribution.
        
        Args:
            validated_data: Validated notification data
            
        Returns:
            Created Notification instance
        """
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['user'] = request.user
        return super().create(validated_data)

class BookStatisticsSerializer(serializers.Serializer):
    """
    Serializer for book statistics data.
    
    This serializer handles aggregated book statistics for API responses.
    """
    total_books = serializers.IntegerField()
    read_books = serializers.IntegerField()
    unread_books = serializers.IntegerField()
    read_percentage = serializers.FloatField()
    unread_percentage = serializers.FloatField()
    most_read_books = BookSerializer(many=True)
    most_viewed_books = BookSerializer(many=True)

class UserStatisticsSerializer(serializers.Serializer):
    """
    Serializer for user statistics data.
    
    This serializer handles aggregated user statistics for API responses.
    """
    total_users = serializers.IntegerField()
    admin_users = serializers.IntegerField()
    regular_users = serializers.IntegerField()
    users = UserSerializer(many=True)

class SystemStatisticsSerializer(serializers.Serializer):
    """
    Serializer for system-wide statistics data.
    
    This serializer handles comprehensive system statistics for API responses.
    """
    book_stats = BookStatisticsSerializer()
    user_stats = UserStatisticsSerializer()
    total_notifications = serializers.IntegerField()
    read_notifications = serializers.IntegerField()
    unread_notifications = serializers.IntegerField()

class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login data.
    
    This serializer handles login credentials for API authentication.
    """
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128, write_only=True)

class PasswordChangeSerializer(serializers.Serializer):
    """
    Serializer for password change data.
    
    This serializer handles password change requests with validation.
    """
    current_password = serializers.CharField(max_length=128, write_only=True)
    new_password = serializers.CharField(max_length=128, write_only=True)
    confirm_new_password = serializers.CharField(max_length=128, write_only=True)
    
    def validate(self, attrs):
        """
        Validate password change data.
        
        Args:
            attrs: Dictionary of field values
            
        Returns:
            Validated attributes
            
        Raises:
            ValidationError: If passwords don't match or validation fails
        """
        if attrs.get('new_password') != attrs.get('confirm_new_password'):
            raise serializers.ValidationError("New passwords do not match.")
        
        if attrs.get('current_password') == attrs.get('new_password'):
            raise serializers.ValidationError("New password must be different from current password.")
        
        return attrs
