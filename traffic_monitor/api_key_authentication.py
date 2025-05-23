# permissions.py
from rest_framework import permissions
from django.conf import settings


class HasAPIKeyOrReadOnly(permissions.BasePermission):
    """
    This model sets a custom permission layer for API Key authentication.
    It checks if the API key provided in the request header matches 
    the one stored in the environment variable.
    """
    API_KEY = settings.API_KEY
    def has_permission(self, request, view):

        if request.method not in permissions.SAFE_METHODS: #POST
            auth_header = request.META.get('HTTP_AUTHORIZATION', '')
            
            if not auth_header.startswith('API-Key '):
                return False
                
            provided_key = auth_header.split(' ')[1]
            return provided_key == self.API_KEY
        if not request.user.is_staff:        
            return False
        return True