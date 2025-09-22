"""
HIPAA Authorization Decorators for Django REST Framework ViewSets
"""

from functools import wraps
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response


def is_hipaa_protected():
    """
    Decorator to protect endpoints that require HIPAA authorization.
    
    Checks if the requesting user has the 'hipaa_authorized' role.
    Can be applied to ViewSet methods or entire ViewSet classes.
    
    Usage:
        @is_hipaa_protected()
        class PatientViewSet(viewsets.ModelViewSet):
            ...
            
        # Or on individual methods:
        @is_hipaa_protected()
        def retrieve(self, request, *args, **kwargs):
            ...
    """
    def decorator(view_func_or_class):
        # Check if this is being applied to a class (ViewSet)
        if hasattr(view_func_or_class, 'dispatch'):
            # This is a ViewSet class
            original_dispatch = view_func_or_class.dispatch
            
            @wraps(original_dispatch)
            def wrapped_dispatch(self, request, *args, **kwargs):
                # Check HIPAA authorization
                if not _check_hipaa_authorization(request):
                    return Response(
                        {
                            'error': 'HIPAA Authorization Required',
                            'message': 'You do not have the required HIPAA authorization to access this resource.',
                            'code': 'HIPAA_UNAUTHORIZED'
                        },
                        status=status.HTTP_403_FORBIDDEN
                    )
                
                return original_dispatch(self, request, *args, **kwargs)
            
            view_func_or_class.dispatch = wrapped_dispatch
            return view_func_or_class
        
        else:
            # This is a method
            @wraps(view_func_or_class)
            def wrapped_view(self, request, *args, **kwargs):
                # Check HIPAA authorization
                if not _check_hipaa_authorization(request):
                    return Response(
                        {
                            'error': 'HIPAA Authorization Required',
                            'message': 'You do not have the required HIPAA authorization to access this resource.',
                            'code': 'HIPAA_UNAUTHORIZED'
                        },
                        status=status.HTTP_403_FORBIDDEN
                    )
                
                return view_func_or_class(self, request, *args, **kwargs)
            
            return wrapped_view
    
    return decorator


def _check_hipaa_authorization(request):
    """
    Internal helper function to check if a user has HIPAA authorization.
    
    Args:
        request: Django request object
        
    Returns:
        bool: True if user has hipaa_authorized role, False otherwise
    """
    # Check if user is authenticated
    if not request.user or not request.user.is_authenticated:
        return False
    
    try:
        # Check if user has a profile with the hipaa_authorized role
        user_profile = request.user.profile
        hipaa_role = user_profile.roles.filter(name='hipaa_authorized').first()
        
        if hipaa_role:
            return True
            
        # Also check if user is superuser (bypass HIPAA check for admins)
        if request.user.is_superuser:
            return True
            
        return False
        
    except AttributeError:
        # User doesn't have a profile or roles relationship
        # Check if user is superuser as fallback
        return request.user.is_superuser if hasattr(request.user, 'is_superuser') else False
    except Exception as e:
        # Log the error in production, for now just return False
        print(f"Error checking HIPAA authorization: {e}")
        return False


def get_hipaa_status(user):
    """
    Utility function to get HIPAA authorization status for a user.
    
    Args:
        user: Django User instance
        
    Returns:
        dict: Status information about user's HIPAA authorization
    """
    if not user or not user.is_authenticated:
        return {
            'authorized': False,
            'reason': 'User not authenticated'
        }
    
    try:
        if user.is_superuser:
            return {
                'authorized': True,
                'reason': 'Superuser access'
            }
            
        user_profile = user.profile
        hipaa_role = user_profile.roles.filter(name='hipaa_authorized').first()
        
        if hipaa_role:
            return {
                'authorized': True,
                'reason': 'Has hipaa_authorized role',
                'role_id': str(hipaa_role.id)
            }
        else:
            return {
                'authorized': False,
                'reason': 'Missing hipaa_authorized role'
            }
            
    except AttributeError as e:
        return {
            'authorized': False,
            'reason': f'Profile or roles not found: {e}'
        }
    except Exception as e:
        return {
            'authorized': False,
            'reason': f'Error checking authorization: {e}'
        }
