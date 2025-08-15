from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.apps import apps
from django.contrib.contenttypes.models import ContentType
import json

from .models import Modification, BaseModel

def get_model_fields(instance):
    """Get all fields from a model instance"""
    return {field.name: getattr(instance, field.name) 
            for field in instance._meta.fields 
            if not field.is_relation and field.name != 'id'}

@receiver(pre_save)
def track_model_changes(sender, instance, **kwargs):
    """Track changes to models that inherit from BaseModel"""
    # Skip if it's not a BaseModel or it's the Modification model itself
    if not isinstance(instance, BaseModel) or sender.__name__ == 'Modification':
        return
    
    # Skip if it's a new instance
    if not instance.pk:
        return
    
    try:
        # Get the old instance from the database
        old_instance = sender.objects.get(pk=instance.pk)
        
        # Get the fields for both instances
        old_fields = get_model_fields(old_instance)
        new_fields = get_model_fields(instance)
        
        # Find changed fields
        for field_name, old_value in old_fields.items():
            new_value = new_fields.get(field_name)
            
            # Skip if the field hasn't changed
            if old_value == new_value:
                continue
            
            # Create a modification record
            content_type = ContentType.objects.get_for_model(instance)
            Modification.objects.create(
                model=sender.__name__,
                content_type=content_type,
                object_id=instance.pk,
                field=field_name,
                before=str(old_value) if old_value is not None else None,
                after=str(new_value) if new_value is not None else None
            )
    except sender.DoesNotExist:
        # This is a new instance, no need to track changes
        pass
    except Exception as e:
        # Log the error but don't prevent the save
        print(f"Error tracking changes: {e}")
