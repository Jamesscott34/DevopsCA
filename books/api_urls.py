"""
URL configuration for the Book Catalog REST API.

This module defines all the API URL patterns for the REST API endpoints.
Each URL pattern maps to a specific ViewSet or API view that handles
the request and returns JSON responses.
"""

from rest_framework.routers import DefaultRouter
from django.urls import path
from .api_views import (
    BookViewSet, UserViewSet, NotificationViewSet, AuthViewSet,
    SystemStatisticsView
)

# Create router for ViewSets
router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')
router.register(r'users', UserViewSet, basename='user')
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'auth', AuthViewSet, basename='auth')

# API URL patterns
urlpatterns = [
    # System statistics endpoint
    path('statistics/', SystemStatisticsView.as_view(), name='api-statistics'),
] + router.urls
