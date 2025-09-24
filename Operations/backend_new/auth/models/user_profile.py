from core.models import BaseModel, Role, Department
from django.contrib.auth.models import User
from django.db import models

class UserProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    # Legacy fields (will be deprecated after migration)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address_line1 = models.CharField(max_length=255, blank=True, null=True)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    zip = models.CharField(max_length=20, blank=True, null=True)

    # HIPAA-compliant encrypted fields
    first_name_encrypted = models.TextField(null=True, blank=True, help_text="Encrypted first name")
    last_name_encrypted = models.TextField(null=True, blank=True, help_text="Encrypted last name")
    email_encrypted = models.TextField(null=True, blank=True, help_text="Encrypted email")
    email_hash = models.CharField(max_length=64, null=True, blank=True, db_index=True, help_text="HMAC hash for email searches")
    phone_encrypted = models.TextField(null=True, blank=True, help_text="Encrypted phone")
    phone_hash = models.CharField(max_length=64, null=True, blank=True, db_index=True, help_text="HMAC hash for phone searches")
    address_line1_encrypted = models.TextField(null=True, blank=True, help_text="Encrypted address line 1")
    address_line2_encrypted = models.TextField(null=True, blank=True, help_text="Encrypted address line 2")
    city_encrypted = models.TextField(null=True, blank=True, help_text="Encrypted city")
    state_encrypted = models.TextField(null=True, blank=True, help_text="Encrypted state")
    country_encrypted = models.TextField(null=True, blank=True, help_text="Encrypted country")
    zip_encrypted = models.TextField(null=True, blank=True, help_text="Encrypted ZIP code")

    # Non-PHI fields
    department_ids = models.ManyToManyField(Department, related_name="users")
    roles = models.ManyToManyField(Role, related_name="users")
    departments = models.ManyToManyField(Department, related_name="department_users")
    flags = models.JSONField(default=list, blank=True)

    # MFA related fields
    mfa_enabled = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)

    def __str__(self):
        # Use encrypted fields if available, fallback to legacy
        first_name = self.get_first_name()
        last_name = self.get_last_name()
        return f"{first_name} {last_name}".strip() or str(self.user.username)

    # Helper methods for backward compatibility during migration
    def get_first_name(self):
        """Get first name, preferring encrypted version."""
        if self.first_name_encrypted:
            try:
                from .encryption import FieldEncryption
                return FieldEncryption.decrypt(self.first_name_encrypted)
            except:
                pass
        return self.first_name or ''

    def get_last_name(self):
        """Get last name, preferring encrypted version."""
        if self.last_name_encrypted:
            try:
                from .encryption import FieldEncryption
                return FieldEncryption.decrypt(self.last_name_encrypted)
            except:
                pass
        return self.last_name or ''

    def get_email(self):
        """Get email, preferring encrypted version."""
        if self.email_encrypted:
            try:
                from .encryption import FieldEncryption
                return FieldEncryption.decrypt(self.email_encrypted)
            except:
                pass
        return self.email or ''

    def get_phone(self):
        """Get phone, preferring encrypted version."""
        if self.phone_encrypted:
            try:
                from .encryption import FieldEncryption
                return FieldEncryption.decrypt(self.phone_encrypted)
            except:
                pass
        return self.phone or ''

    def get_address_line1(self):
        """Get address line 1, preferring encrypted version."""
        if self.address_line1_encrypted:
            try:
                from .encryption import FieldEncryption
                return FieldEncryption.decrypt(self.address_line1_encrypted)
            except:
                pass
        return self.address_line1 or ''

    def get_address_line2(self):
        """Get address line 2, preferring encrypted version."""
        if self.address_line2_encrypted:
            try:
                from .encryption import FieldEncryption
                return FieldEncryption.decrypt(self.address_line2_encrypted)
            except:
                pass
        return self.address_line2 or ''

    def get_city(self):
        """Get city, preferring encrypted version."""
        if self.city_encrypted:
            try:
                from .encryption import FieldEncryption
                return FieldEncryption.decrypt(self.city_encrypted)
            except:
                pass
        return self.city or ''

    def get_state(self):
        """Get state, preferring encrypted version."""
        if self.state_encrypted:
            try:
                from .encryption import FieldEncryption
                return FieldEncryption.decrypt(self.state_encrypted)
            except:
                pass
        return self.state or ''

    def get_country(self):
        """Get country, preferring encrypted version."""
        if self.country_encrypted:
            try:
                from .encryption import FieldEncryption
                return FieldEncryption.decrypt(self.country_encrypted)
            except:
                pass
        return self.country or ''

    def get_zip(self):
        """Get ZIP code, preferring encrypted version."""
        if self.zip_encrypted:
            try:
                from .encryption import FieldEncryption
                return FieldEncryption.decrypt(self.zip_encrypted)
            except:
                pass
        return self.zip or ''

    def save(self, *args, **kwargs):
        """Override save to automatically encrypt PHI fields."""
        from .encryption import FieldEncryption
        import logging

        logger = logging.getLogger(__name__)

        # Define fields that need encryption for UserProfile
        text_fields = [
            'first_name', 'last_name', 'email', 'phone',
            'address_line1', 'address_line2', 'city', 'state', 'zip', 'country'
        ]
        searchable_fields = ['email', 'phone']

        # Encrypt text fields
        for field_name in text_fields:
            value = getattr(self, field_name, None)
            if value and not getattr(self, f"{field_name}_encrypted", None):
                try:
                    # Encrypt the value
                    encrypted_value = FieldEncryption.encrypt(str(value))
                    setattr(self, f"{field_name}_encrypted", encrypted_value)

                    # Generate search hash for searchable fields
                    if field_name in searchable_fields:
                        search_hash = FieldEncryption.generate_search_hash(str(value))
                        setattr(self, f"{field_name}_hash", search_hash)
                except Exception as e:
                    logger.warning(f"Could not encrypt UserProfile {field_name}: {str(e)}")
                    # Continue saving - don't block the save operation

        # Call parent save
        super().save(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=['email_hash']),
            models.Index(fields=['phone_hash']),
        ]