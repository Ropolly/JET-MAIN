from django.db import models
from django.contrib.auth.models import User
import uuid
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class BaseModel(models.Model):
    """Base model with common fields for all entities."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="%(class)s_created")
    modified_on = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="%(class)s_modified"
    )
    status = models.CharField(max_length=50, default="active", db_index=True)
    lock = models.BooleanField(default=False)
    
    class Meta:
        abstract = True


class Modification(models.Model):
    """Model for tracking changes to other models."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    model = models.CharField(max_length=100)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    model_key = GenericForeignKey('content_type', 'object_id')
    field = models.CharField(max_length=100)
    before = models.TextField(null=True, blank=True)
    after = models.TextField(null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="modifications")
    
    class Meta:
        ordering = ['-time']
        
    def __str__(self):
        return f"{self.model} - {self.field} - {self.time}"


class Comment(models.Model):
    """Comments attached to any model instance via a generic foreign key."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    text = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="comments_created")
    
    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]
        ordering = ['-created_on']
    
    def __str__(self):
        return f"Comment on {self.content_object} by {self.created_by}"
