from django.contrib.contenttypes.models import ContentType
from .models import Modification
from .signals import get_current_user


def track_modification(instance, field_name, before_value, after_value, user=None):
    """
    Manually track a modification for cases where signals aren't sufficient
    
    Args:
        instance: The model instance that was modified
        field_name: The name of the field that changed
        before_value: The previous value
        after_value: The new value  
        user: The user making the change (optional, will use thread-local if not provided)
    """
    if user is None:
        user = get_current_user()
    
    content_type = ContentType.objects.get_for_model(instance)
    
    Modification.objects.create(
        model=instance.__class__.__name__,
        content_type=content_type,
        object_id=instance.pk,
        field=field_name,
        before=str(before_value) if before_value is not None else None,
        after=str(after_value) if after_value is not None else None,
        user=user
    )


def track_creation(instance, user=None):
    """
    Track the creation of a new model instance
    
    Args:
        instance: The newly created model instance
        user: The user creating the instance (optional, will use thread-local if not provided)
    """
    if user is None:
        user = get_current_user()
    
    content_type = ContentType.objects.get_for_model(instance)
    
    Modification.objects.create(
        model=instance.__class__.__name__,
        content_type=content_type,
        object_id=instance.pk,
        field='__created__',
        before=None,
        after='Instance created',
        user=user
    )


def track_deletion(instance, user=None):
    """
    Track the deletion of a model instance
    
    Args:
        instance: The model instance being deleted
        user: The user deleting the instance (optional, will use thread-local if not provided)
    """
    if user is None:
        user = get_current_user()
    
    content_type = ContentType.objects.get_for_model(instance)
    
    Modification.objects.create(
        model=instance.__class__.__name__,
        content_type=content_type,
        object_id=instance.pk,
        field='__deleted__',
        before='Instance existed',
        after=None,
        user=user
    )