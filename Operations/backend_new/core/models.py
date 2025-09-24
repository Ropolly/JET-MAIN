from django.db import models
from django.contrib.auth.models import User


class BaseModel(models.Model):
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

# Modifications model for tracking changes
class Modification(models.Model):
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

# Permission model
class Permission(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

# Role model
class Role(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    permissions = models.ManyToManyField(Permission, related_name="roles")
    
    def __str__(self):
        return self.name

# Department model
class Department(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    permission_ids = models.ManyToManyField(Permission, related_name="departments")
    
    def __str__(self):
        return self.name

class Contact(BaseModel):
    # Legacy fields (will be deprecated after migration)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    business_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address_line1 = models.CharField(max_length=255, blank=True, null=True)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zip = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    nationality = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    passport_number = models.CharField(max_length=100, blank=True, null=True)
    passport_expiration_date = models.DateField(blank=True, null=True)

    # HIPAA-compliant encrypted fields
    first_name_encrypted = models.TextField(null=True, blank=True, help_text="Encrypted first name")
    last_name_encrypted = models.TextField(null=True, blank=True, help_text="Encrypted last name")
    business_name_encrypted = models.TextField(null=True, blank=True, help_text="Encrypted business name")
    email_encrypted = models.TextField(null=True, blank=True, help_text="Encrypted email")
    email_hash = models.CharField(max_length=64, null=True, blank=True, db_index=True, help_text="HMAC hash for email searches")
    phone_encrypted = models.TextField(null=True, blank=True, help_text="Encrypted phone")
    phone_hash = models.CharField(max_length=64, null=True, blank=True, db_index=True, help_text="HMAC hash for phone searches")
    address_line1_encrypted = models.TextField(null=True, blank=True, help_text="Encrypted address line 1")
    address_line2_encrypted = models.TextField(null=True, blank=True, help_text="Encrypted address line 2")
    city_encrypted = models.TextField(null=True, blank=True, help_text="Encrypted city")
    state_encrypted = models.TextField(null=True, blank=True, help_text="Encrypted state")
    zip_encrypted = models.TextField(null=True, blank=True, help_text="Encrypted ZIP code")
    country_encrypted = models.TextField(null=True, blank=True, help_text="Encrypted country")
    nationality_encrypted = models.TextField(null=True, blank=True, help_text="Encrypted nationality")
    date_of_birth_encrypted = models.TextField(null=True, blank=True, help_text="Encrypted date of birth")
    passport_number_encrypted = models.TextField(null=True, blank=True, help_text="Encrypted passport number")
    passport_number_hash = models.CharField(max_length=64, null=True, blank=True, db_index=True, help_text="HMAC hash for passport searches")
    passport_expiration_date_encrypted = models.TextField(null=True, blank=True, help_text="Encrypted passport expiration date")

    def __str__(self):
        business_name = self.get_business_name()
        if business_name:
            return business_name
        first_name = self.get_first_name()
        last_name = self.get_last_name()
        return f"{first_name} {last_name}".strip() or "Contact"

    def clean(self):
        first_name = self.get_first_name()
        last_name = self.get_last_name()
        business_name = self.get_business_name()

        if not first_name and not last_name and not business_name:
            raise models.ValidationError("Either first/last name or business name is required")

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

    def get_business_name(self):
        """Get business name, preferring encrypted version."""
        if self.business_name_encrypted:
            try:
                from .encryption import FieldEncryption
                return FieldEncryption.decrypt(self.business_name_encrypted)
            except:
                pass
        return self.business_name or ''

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

    def get_date_of_birth(self):
        """Get date of birth, preferring encrypted version."""
        if self.date_of_birth_encrypted:
            try:
                from .encryption import FieldEncryption
                from datetime import datetime
                date_str = FieldEncryption.decrypt(self.date_of_birth_encrypted)
                return datetime.fromisoformat(date_str).date()
            except:
                pass
        return self.date_of_birth

    def get_passport_number(self):
        """Get passport number, preferring encrypted version."""
        if self.passport_number_encrypted:
            try:
                from .encryption import FieldEncryption
                return FieldEncryption.decrypt(self.passport_number_encrypted)
            except:
                pass
        return self.passport_number or ''

    def get_passport_expiration_date(self):
        """Get passport expiration date, preferring encrypted version."""
        if self.passport_expiration_date_encrypted:
            try:
                from .encryption import FieldEncryption
                from datetime import datetime
                date_str = FieldEncryption.decrypt(self.passport_expiration_date_encrypted)
                return datetime.fromisoformat(date_str).date()
            except:
                pass
        return self.passport_expiration_date

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

    def get_zip(self):
        """Get ZIP code, preferring encrypted version."""
        if self.zip_encrypted:
            try:
                from .encryption import FieldEncryption
                return FieldEncryption.decrypt(self.zip_encrypted)
            except:
                pass
        return self.zip or ''

    def get_country(self):
        """Get country, preferring encrypted version."""
        if self.country_encrypted:
            try:
                from .encryption import FieldEncryption
                return FieldEncryption.decrypt(self.country_encrypted)
            except:
                pass
        return self.country or ''

    def get_nationality(self):
        """Get nationality, preferring encrypted version."""
        if self.nationality_encrypted:
            try:
                from .encryption import FieldEncryption
                return FieldEncryption.decrypt(self.nationality_encrypted)
            except:
                pass
        return self.nationality or ''

    def save(self, *args, **kwargs):
        """Override save to automatically encrypt PHI fields."""
        from .encryption import FieldEncryption
        import logging

        logger = logging.getLogger(__name__)

        # Define fields that need encryption
        text_fields = [
            'first_name', 'last_name', 'business_name', 'email', 'phone',
            'address_line1', 'address_line2', 'city', 'state', 'zip',
            'country', 'nationality', 'passport_number'
        ]
        date_fields = ['date_of_birth', 'passport_expiration_date']
        searchable_fields = ['email', 'phone', 'passport_number']

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
                    logger.warning(f"Could not encrypt {field_name}: {str(e)}")
                    # Continue saving - don't block the save operation

        # Encrypt date fields
        for field_name in date_fields:
            value = getattr(self, field_name, None)
            if value and not getattr(self, f"{field_name}_encrypted", None):
                try:
                    # Convert date to ISO format string for encryption
                    encrypted_value = FieldEncryption.encrypt(value.isoformat())
                    setattr(self, f"{field_name}_encrypted", encrypted_value)
                except Exception as e:
                    logger.warning(f"Could not encrypt {field_name}: {str(e)}")
                    # Continue saving - don't block the save operation

        # Call parent save
        super().save(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=['email_hash']),
            models.Index(fields=['phone_hash']),
            models.Index(fields=['passport_number_hash']),
        ]