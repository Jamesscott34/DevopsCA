from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from .models import User

class CustomSessionAuthentication(BaseAuthentication):
    def authenticate(self, request):
        print("DEBUG: Session keys:", list(request.session.keys()))
        user_id = request.session.get('user_id')
        print("DEBUG: user_id from session:", user_id)
        if not user_id:
            return None
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')
        return (user, None) 