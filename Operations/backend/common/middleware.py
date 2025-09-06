from django.utils.deprecation import MiddlewareMixin
import threading

# Thread-local storage for current user
_thread_locals = threading.local()


def get_current_user():
    """Get the current user from thread-local storage."""
    return getattr(_thread_locals, 'user', None)


def set_current_user(user):
    """Set the current user in thread-local storage."""
    _thread_locals.user = user


class CurrentUserMiddleware(MiddlewareMixin):
    """
    Middleware to set the current user in thread-local storage
    for use in modification tracking and audit trails.
    """
    
    def process_request(self, request):
        """Set the current user at the start of each request."""
        user = getattr(request, 'user', None)
        if user and user.is_authenticated:
            set_current_user(user)
        else:
            set_current_user(None)
        return None
    
    def process_response(self, request, response):
        """Clear the current user after the request is complete."""
        set_current_user(None)
        return response
    
    def process_exception(self, request, exception):
        """Clear the current user if an exception occurs."""
        set_current_user(None)
        return None
