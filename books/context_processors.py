"""
Context processors for the Book Catalog application.

This module provides context processors that add data to all templates
automatically, such as user information and notification counts.
"""

from .models import Notification

def notification_count(request):
    """
    Context processor to add unread notification count to all templates.
    
    This processor checks if a user is logged in and adds their unread
    notification count to the template context for display in the navigation.
    
    Args:
        request: Django HttpRequest object
        
    Returns:
        Dictionary containing unread_notifications_count
    """
    unread_count = 0
    
    # Check if user is logged in (using session)
    if 'user_id' in request.session:
        try:
            from .models import User
            user = User.objects.get(id=request.session['user_id'])
            unread_count = Notification.objects.filter(user=user, is_read=False).count()
        except User.DoesNotExist:
            pass
    
    return {
        'unread_notifications_count': unread_count
    } 