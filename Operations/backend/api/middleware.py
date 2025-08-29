from django.utils.deprecation import MiddlewareMixin
from .signals import set_current_user


class CurrentUserMiddleware(MiddlewareMixin):
    """
    Middleware to set the current user in thread-local storage
    for use in modification tracking
    """
    
    def process_request(self, request):
        """Set the current user at the start of each request"""
        user = getattr(request, 'user', None)
        if user and user.is_authenticated:
            set_current_user(user)
        else:
            set_current_user(None)
        return None
    
    def process_response(self, request, response):
        """Clear the current user after the request is complete"""
        set_current_user(None)
        return response
    
    def process_exception(self, request, exception):
        """Clear the current user if an exception occurs"""
        set_current_user(None)
        return None