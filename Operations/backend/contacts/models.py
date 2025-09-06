from django.db import models
from common.models import BaseModel


class Contact(BaseModel):
    """Contact model for customers, crew, and other personnel."""
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    business_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    
    # Address information
    address_line1 = models.CharField(max_length=255, blank=True, null=True)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zip = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    
    # Travel document information
    nationality = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    passport_number = models.CharField(max_length=100, blank=True, null=True)
    passport_expiration_date = models.DateField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['first_name', 'last_name']),
            models.Index(fields=['business_name']),
            models.Index(fields=['email']),
        ]

    def __str__(self):
        if self.business_name:
            return self.business_name
        return f"{self.first_name} {self.last_name}".strip() or "Unnamed Contact"
    
    def clean(self):
        """Validate that either name or business name is provided."""
        if not self.first_name and not self.last_name and not self.business_name:
            raise models.ValidationError("Either first/last name or business name is required")
    
    @property
    def full_name(self):
        """Return full name or business name."""
        if self.business_name:
            return self.business_name
        return f"{self.first_name} {self.last_name}".strip()


class FBO(BaseModel):
    """Fixed Base Operator model for airport services."""
    name = models.CharField(max_length=255)
    
    # Address information
    address_line1 = models.CharField(max_length=255, blank=True, null=True)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zip = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    
    # Contact information
    contacts = models.ManyToManyField(Contact, related_name="fbos")
    phone = models.CharField(max_length=20, blank=True, null=True)
    phone_secondary = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['city', 'state']),
        ]
        verbose_name = "FBO"
        verbose_name_plural = "FBOs"
    
    def __str__(self):
        return self.name


class Ground(BaseModel):
    """Ground Transportation model for airport ground services."""
    name = models.CharField(max_length=255)
    
    # Address information
    address_line1 = models.CharField(max_length=255, blank=True, null=True)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zip = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    
    # Contact information and notes
    notes = models.TextField(blank=True, null=True)
    contacts = models.ManyToManyField(Contact, related_name="grounds")

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['city', 'state']),
        ]
        verbose_name = "Ground Transportation"
        verbose_name_plural = "Ground Transportation"
    
    def __str__(self):
        return self.name
