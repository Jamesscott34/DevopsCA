"""
Django REST Framework API views for the Book Catalog application.

This module defines API views that handle HTTP requests and return JSON responses.
Views include authentication, permissions, and comprehensive CRUD operations
for all models in the application.
"""

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import get_object_or_404
from django.db.models import Q, Count
from .models import Book, User, Notification
from .serializer import (
    BookSerializer, UserSerializer, NotificationSerializer,
    BookStatisticsSerializer, UserStatisticsSerializer, SystemStatisticsSerializer,
    LoginSerializer, PasswordChangeSerializer
)

class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Book model with comprehensive CRUD operations.
    
    This ViewSet provides full CRUD functionality for books, including
    filtering, searching, and statistics. It handles user authentication
    and proper book attribution.
    """
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Get queryset based on user permissions and filters.
        
        Returns:
            Filtered queryset of books
        """
        user = self.request.user
        queryset = Book.objects.all()
        
        # Admin can see all books, regular users see their own
        if user.username != 'admin':
            queryset = queryset.filter(added_by=user)
        
        # Apply filters
        is_read = self.request.query_params.get('is_read', None)
        if is_read is not None:
            queryset = queryset.filter(is_read=is_read.lower() == 'true')
        
        # Search functionality
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(author__icontains=search) |
                Q(description__icontains=search)
            )
        
        return queryset.order_by('-created_at')
    
    def perform_create(self, serializer):
        """
        Create a book with user attribution.
        
        Args:
            serializer: Book serializer instance
        """
        serializer.save(added_by=self.request.user)
    
    @action(detail=True, methods=['post'])
    def toggle_read(self, request, pk=None):
        """
        Toggle the read status of a book.
        
        Args:
            request: HTTP request
            pk: Primary key of the book
            
        Returns:
            Updated book data
        """
        book = self.get_object()
        book.is_read = not book.is_read
        book.save()
        serializer = self.get_serializer(book)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def read_books(self, request):
        """
        Get all read books.
        
        Args:
            request: HTTP request
            
        Returns:
            List of read books
        """
        queryset = self.get_queryset().filter(is_read=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def unread_books(self, request):
        """
        Get all unread books.
        
        Args:
            request: HTTP request
            
        Returns:
            List of unread books
        """
        queryset = self.get_queryset().filter(is_read=False)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """
        Get book statistics for the current user.
        
        Args:
            request: HTTP request
            
        Returns:
            Book statistics data
        """
        user = request.user
        queryset = self.get_queryset()
        
        total_books = queryset.count()
        read_books = queryset.filter(is_read=True).count()
        unread_books = queryset.filter(is_read=False).count()
        
        read_percentage = (read_books / total_books * 100) if total_books > 0 else 0
        unread_percentage = (unread_books / total_books * 100) if total_books > 0 else 0
        
        most_read_books = queryset.filter(is_read=True).order_by('-view_count')[:5]
        most_viewed_books = queryset.order_by('-view_count')[:5]
        
        data = {
            'total_books': total_books,
            'read_books': read_books,
            'unread_books': unread_books,
            'read_percentage': round(read_percentage, 2),
            'unread_percentage': round(unread_percentage, 2),
            'most_read_books': BookSerializer(most_read_books, many=True).data,
            'most_viewed_books': BookSerializer(most_viewed_books, many=True).data,
        }
        
        serializer = BookStatisticsSerializer(data)
        return Response(serializer.data)

class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for User model with admin-only access.
    
    This ViewSet provides user management functionality for admin users only.
    Regular users cannot access user data through the API.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Get queryset based on user permissions.
        
        Returns:
            Filtered queryset of users
        """
        user = self.request.user
        if user.username == 'admin':
            return User.objects.all().order_by('-created_at')
        return User.objects.none()
    
    def perform_create(self, serializer):
        """
        Create a user with hashed password.
        
        Args:
            serializer: User serializer instance
        """
        serializer.save()
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """
        Get user statistics (admin only).
        
        Args:
            request: HTTP request
            
        Returns:
            User statistics data
        """
        if request.user.username != 'admin':
            return Response({'error': 'Admin access required'}, status=status.HTTP_403_FORBIDDEN)
        
        total_users = User.objects.count()
        admin_users = User.objects.filter(username='admin').count()
        regular_users = total_users - admin_users
        users = User.objects.all().order_by('-created_at')
        
        data = {
            'total_users': total_users,
            'admin_users': admin_users,
            'regular_users': regular_users,
            'users': UserSerializer(users, many=True).data,
        }
        
        serializer = UserStatisticsSerializer(data)
        return Response(serializer.data)

class NotificationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Notification model with user-specific access.
    
    This ViewSet provides notification functionality for users to view
    their own notifications and for admins to manage all notifications.
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Get queryset based on user permissions.
        
        Returns:
            Filtered queryset of notifications
        """
        user = self.request.user
        if user.username == 'admin':
            return Notification.objects.all().order_by('-created_at')
        return Notification.objects.filter(user=user).order_by('-created_at')
    
    def perform_create(self, serializer):
        """
        Create a notification with user attribution.
        
        Args:
            serializer: Notification serializer instance
        """
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """
        Mark a notification as read.
        
        Args:
            request: HTTP request
            pk: Primary key of the notification
            
        Returns:
            Updated notification data
        """
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        serializer = self.get_serializer(notification)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """
        Mark all notifications as read for the current user.
        
        Args:
            request: HTTP request
            
        Returns:
            Success message
        """
        user = request.user
        unread_notifications = Notification.objects.filter(user=user, is_read=False)
        count = unread_notifications.count()
        unread_notifications.update(is_read=True)
        
        return Response({
            'message': f'{count} notification(s) marked as read.',
            'count': count
        })
    
    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """
        Get count of unread notifications for the current user.
        
        Args:
            request: HTTP request
            
        Returns:
            Unread notification count
        """
        user = request.user
        count = Notification.objects.filter(user=user, is_read=False).count()
        return Response({'unread_count': count})

class AuthViewSet(viewsets.ViewSet):
    """
    ViewSet for authentication operations.
    
    This ViewSet handles user registration, login, logout, and password changes
    through the API.
    """
    permission_classes = [permissions.AllowAny]
    
    @action(detail=False, methods=['post'])
    def register(self, request):
        """
        Register a new user.
        
        Args:
            request: HTTP request with user data
            
        Returns:
            Created user data or error messages
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'User registered successfully.',
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        """
        Authenticate user and return session data.
        
        Args:
            request: HTTP request with login credentials
            
        Returns:
            Authentication result
        """
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            try:
                user = User.objects.get(username=username)
                if check_password(password, user.password):
                    # Set session
                    request.session['user_id'] = user.id
                    return Response({
                        'message': 'Login successful.',
                        'user': UserSerializer(user).data,
                        'is_admin': user.username == 'admin'
                    })
                else:
                    return Response({
                        'error': 'Invalid credentials.'
                    }, status=status.HTTP_401_UNAUTHORIZED)
            except User.DoesNotExist:
                return Response({
                    'error': 'Invalid credentials.'
                }, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def logout(self, request):
        """
        Logout user and clear session.
        
        Args:
            request: HTTP request
            
        Returns:
            Logout confirmation
        """
        request.session.flush()
        return Response({'message': 'Logout successful.'})
    
    @action(detail=False, methods=['post'])
    def change_password(self, request):
        """
        Change user password.
        
        Args:
            request: HTTP request with password data
            
        Returns:
            Password change result
        """
        if not request.user.is_authenticated:
            return Response({
                'error': 'Authentication required.'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            current_password = serializer.validated_data['current_password']
            new_password = serializer.validated_data['new_password']
            
            if check_password(current_password, user.password):
                user.password = make_password(new_password)
                user.save()
                return Response({'message': 'Password changed successfully.'})
            else:
                return Response({
                    'error': 'Current password is incorrect.'
                }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SystemStatisticsView(APIView):
    """
    API view for system-wide statistics.
    
    This view provides comprehensive system statistics for admin users.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """
        Get system-wide statistics.
        
        Args:
            request: HTTP request
            
        Returns:
            System statistics data
        """
        if request.user.username != 'admin':
            return Response({
                'error': 'Admin access required.'
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Book statistics
        total_books = Book.objects.count()
        read_books = Book.objects.filter(is_read=True).count()
        unread_books = Book.objects.filter(is_read=False).count()
        read_percentage = (read_books / total_books * 100) if total_books > 0 else 0
        unread_percentage = (unread_books / total_books * 100) if total_books > 0 else 0
        
        most_read_books = Book.objects.filter(is_read=True).order_by('-view_count')[:5]
        most_viewed_books = Book.objects.order_by('-view_count')[:5]
        
        # User statistics
        total_users = User.objects.count()
        admin_users = User.objects.filter(username='admin').count()
        regular_users = total_users - admin_users
        users = User.objects.all().order_by('-created_at')
        
        # Notification statistics
        total_notifications = Notification.objects.count()
        read_notifications = Notification.objects.filter(is_read=True).count()
        unread_notifications = Notification.objects.filter(is_read=False).count()
        
        data = {
            'book_stats': {
                'total_books': total_books,
                'read_books': read_books,
                'unread_books': unread_books,
                'read_percentage': round(read_percentage, 2),
                'unread_percentage': round(unread_percentage, 2),
                'most_read_books': BookSerializer(most_read_books, many=True).data,
                'most_viewed_books': BookSerializer(most_viewed_books, many=True).data,
            },
            'user_stats': {
                'total_users': total_users,
                'admin_users': admin_users,
                'regular_users': regular_users,
                'users': UserSerializer(users, many=True).data,
            },
            'total_notifications': total_notifications,
            'read_notifications': read_notifications,
            'unread_notifications': unread_notifications,
        }
        
        serializer = SystemStatisticsSerializer(data)
        return Response(serializer.data)
