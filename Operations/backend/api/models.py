from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Base model with default fields
class BaseModel(models.Model):
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

# Modifications model for tracking changes
class Modification(models.Model):
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

# Custom User model extending Django's User model
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

    class Meta:
        indexes = [
            models.Index(fields=['email_hash']),
            models.Index(fields=['phone_hash']),
        ]


# User Activation Token model for email-based user creation and password reset
class UserActivationToken(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="activation_tokens")
    token_hash = models.CharField(max_length=64, unique=True, null=True, blank=True, help_text="SHA-256 hash of the token")
    email = models.EmailField()
    token_type = models.CharField(max_length=20, choices=[
        ('activation', 'Account Activation'),
        ('password_reset', 'Password Reset')
    ], default='activation')
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    used_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['token_hash']),
            models.Index(fields=['email', 'token_type']),
            models.Index(fields=['expires_at', 'is_used']),
        ]

    def __str__(self):
        return f"{self.token_type} token for {self.email}"

    @classmethod
    def create_token(cls, user, email, token_type='activation', expires_in_hours=24):
        """Create a new activation token with secure hash storage."""
        import secrets
        import hashlib
        from django.utils import timezone
        from datetime import timedelta

        # Generate a cryptographically secure random token
        token = secrets.token_urlsafe(32)

        # Create SHA-256 hash of the token for storage
        token_hash = hashlib.sha256(token.encode()).hexdigest()

        # Set expiration time
        expires_at = timezone.now() + timedelta(hours=expires_in_hours)

        # Create the token record
        activation_token = cls.objects.create(
            user=user,
            token_hash=token_hash,
            email=email,
            token_type=token_type,
            expires_at=expires_at
        )

        # Return both the token record and the raw token (for sending to user)
        return activation_token, token

    @classmethod
    def verify_token(cls, token, email, token_type='activation'):
        """Verify a token against stored hash."""
        import hashlib
        from django.utils import timezone

        if not token:
            return None

        # Hash the provided token
        token_hash = hashlib.sha256(token.encode()).hexdigest()

        try:
            # Find the token record
            activation_token = cls.objects.get(
                token_hash=token_hash,
                email=email,
                token_type=token_type,
                is_used=False,
                expires_at__gt=timezone.now()
            )
            return activation_token
        except cls.DoesNotExist:
            return None

    def mark_as_used(self):
        """Mark this token as used."""
        from django.utils import timezone
        self.is_used = True
        self.used_at = timezone.now()
        self.save()

    def is_valid(self):
        """Check if token is still valid (not used and not expired)"""
        from django.utils import timezone
        return not self.is_used and self.expires_at > timezone.now()


# Contact model
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

    class Meta:
        indexes = [
            models.Index(fields=['email_hash']),
            models.Index(fields=['phone_hash']),
            models.Index(fields=['passport_number_hash']),
        ]

# FBO (Fixed Base Operator) model
class FBO(BaseModel):
    name = models.CharField(max_length=255)
    address_line1 = models.CharField(max_length=255, blank=True, null=True)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zip = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    contacts = models.ManyToManyField(Contact, related_name="fbos")
    phone = models.CharField(max_length=20, blank=True, null=True)
    phone_secondary = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    
    def __str__(self):
        return self.name

# Ground Transportation model
class Ground(BaseModel):
    name = models.CharField(max_length=255)
    address_line1 = models.CharField(max_length=255, blank=True, null=True)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zip = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    contacts = models.ManyToManyField(Contact, related_name="grounds")

    
    def __str__(self):
        return self.name


class AirportType(models.TextChoices):
    LARGE = 'large_airport', 'Large airport'
    MEDIUM = 'medium_airport', 'Medium airport'
    SMALL = 'small_airport', 'Small airport'


# Airport model
class Airport(BaseModel):
    ident = models.CharField(max_length=10, unique=True, db_index=True)
    name = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    elevation = models.IntegerField(blank=True, null=True)
    iso_country = models.CharField(max_length=100)
    iso_region = models.CharField(max_length=100, blank=True, null=True)
    municipality = models.CharField(max_length=100, blank=True, null=True)
    icao_code = models.CharField(max_length=4, unique=True, db_index=True, blank=True, null=True)
    iata_code = models.CharField(max_length=3, db_index=True, blank=True, null=True)
    local_code = models.CharField(max_length=10, blank=True, null=True)
    gps_code = models.CharField(max_length=20, blank=True, null=True)
    airport_type = models.CharField(
        max_length=20,
        choices=AirportType.choices,
        default=AirportType.SMALL,
        db_index=True,
    )
    fbos = models.ManyToManyField(FBO, related_name="airports", blank=True)
    grounds = models.ManyToManyField(Ground, related_name="airports", blank=True)

    timezone = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} ({self.icao_code}/{self.iata_code})"

# Document model (for file storage)
class Document(models.Model):
    DOCUMENT_TYPES = [
        ('gendec', 'General Declaration'),
        ('quote', 'Quote Form'),
        ('customer_itinerary', 'Customer Itinerary'),
        ('internal_itinerary', 'Internal Itinerary'),
        ('payment_agreement', 'Payment Agreement'),
        ('consent_transport', 'Consent for Transport'),
        ('psa', 'Patient Service Agreement'),
        ('handling_request', 'Handling Request'),
        ('letter_of_medical_necessity', 'Letter of Medical Necessity'),
        ('insurance_card', 'Insurance Card'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    filename = models.CharField(max_length=255)
    content = models.BinaryField(null=True, blank=True)  # Making it optional since we'll use file_path
    file_path = models.CharField(max_length=500, blank=True, null=True)  # Path to file on filesystem
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPES, null=True, blank=True)
    flag = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    
    # Relationships - each document can belong to one of these
    trip = models.ForeignKey('Trip', on_delete=models.CASCADE, related_name='documents', null=True, blank=True)
    contact = models.ForeignKey('Contact', on_delete=models.CASCADE, related_name='documents', null=True, blank=True)
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, related_name='patient_documents', null=True, blank=True)
    passenger = models.ForeignKey('Passenger', on_delete=models.CASCADE, related_name='passenger_documents', null=True, blank=True)
    created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='created_documents')
    
    def __str__(self):
        doc_type = dict(self.DOCUMENT_TYPES).get(self.document_type, 'Document')
        return f"{doc_type}: {self.filename}"

# Aircraft model
class Aircraft(BaseModel):
    tail_number = models.CharField(max_length=20, unique=True, db_index=True)
    company = models.CharField(max_length=255)
    mgtow = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Maximum Gross Takeoff Weight")
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.tail_number} - {self.make} {self.model}"

# Transaction model
class Transaction(BaseModel):
    key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=[
        ("credit_card", "Credit Card"),
        ("ACH", "ACH Transfer")
    ])
    payment_status = models.CharField(max_length=20, choices=[
        ("created", "Created"),
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("failed", "Failed")
    ], default="created")
    payment_date = models.DateTimeField(default=timezone.now)
    email = models.EmailField()
    authorize_net_trans_id = models.CharField(max_length=50, blank=True, null=True, help_text="Authorize.Net Transaction ID")
    
    def __str__(self):
        return f"Transaction {self.key} - {self.amount} - {self.payment_status}"

# Agreement model
class Agreement(BaseModel):
    # Legacy PHI fields (will be deprecated after migration)
    destination_email = models.EmailField()

    # HIPAA-compliant encrypted fields
    destination_email_encrypted = models.TextField(null=True, blank=True, help_text="Encrypted destination email")
    destination_email_hash = models.CharField(max_length=64, null=True, blank=True, db_index=True, help_text="HMAC hash for email searches")

    document_unsigned = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True, blank=True, related_name="unsigned_agreements", db_column="document_unsigned_id")
    document_signed = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True, blank=True, related_name="signed_agreements", db_column="document_signed_id")
    status = models.CharField(max_length=20, choices=[
        ("created", "Created"),
        ("pending", "Pending"),
        ("modified", "Modified"),
        ("signed", "Signed"),
        ("denied", "Denied")
    ], default="created")

    def __str__(self):
        return f"Agreement for {self.get_destination_email()} - {self.status}"

    # Helper methods for backward compatibility during migration
    def get_destination_email(self):
        """Get destination email, preferring encrypted version."""
        if self.destination_email_encrypted:
            try:
                from .encryption import FieldEncryption
                return FieldEncryption.decrypt(self.destination_email_encrypted)
            except:
                pass
        return self.destination_email or ''

    class Meta:
        indexes = [
            models.Index(fields=['destination_email_hash']),
        ]

# Patient model
class Patient(BaseModel):
    info = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="patients")
    bed_at_origin = models.BooleanField(default=False)
    bed_at_destination = models.BooleanField(default=False)

    # Legacy PHI fields (will be deprecated after migration)
    date_of_birth = models.DateField()
    nationality = models.CharField(max_length=100)
    passport_number = models.CharField(max_length=100)
    passport_expiration_date = models.DateField()
    special_instructions = models.TextField(blank=True, null=True)

    # HIPAA-compliant encrypted fields
    date_of_birth_encrypted = models.TextField(null=True, blank=True, help_text="Encrypted date of birth")
    nationality_encrypted = models.TextField(null=True, blank=True, help_text="Encrypted nationality")
    passport_number_encrypted = models.TextField(null=True, blank=True, help_text="Encrypted passport number")
    passport_number_hash = models.CharField(max_length=64, null=True, blank=True, db_index=True, help_text="HMAC hash for passport searches")
    passport_expiration_date_encrypted = models.TextField(null=True, blank=True, help_text="Encrypted passport expiration date")
    special_instructions_encrypted = models.TextField(null=True, blank=True, help_text="Encrypted special instructions")

    passport_document = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True, blank=True, related_name="passport_patients", db_column="passport_document_id")
    status = models.CharField(max_length=20, choices=[
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("active", "Active"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled")
    ], default="pending", db_index=True)
    letter_of_medical_necessity = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True, blank=True, related_name="medical_necessity_patients", db_column="letter_of_medical_necessity_id")
    insurance_card = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True, blank=True, related_name="insurance_card_patients", db_column="insurance_card_id")

    def __str__(self):
        return f"Patient: {self.info}"

    # Helper methods for backward compatibility during migration
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

    def get_nationality(self):
        """Get nationality, preferring encrypted version."""
        if self.nationality_encrypted:
            try:
                from .encryption import FieldEncryption
                return FieldEncryption.decrypt(self.nationality_encrypted)
            except:
                pass
        return self.nationality or ''

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

    def get_special_instructions(self):
        """Get special instructions, preferring encrypted version."""
        if self.special_instructions_encrypted:
            try:
                from .encryption import FieldEncryption
                return FieldEncryption.decrypt(self.special_instructions_encrypted)
            except:
                pass
        return self.special_instructions or ''

    class Meta:
        indexes = [
            models.Index(fields=['passport_number_hash']),
        ]

# LostReason model for tracking why quotes are lost
class LostReason(BaseModel):
    reason = models.CharField(max_length=30, unique=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.reason
    
    class Meta:
        ordering = ['reason']

# Quote model
class Quote(BaseModel):
    quoted_amount = models.DecimalField(max_digits=10, decimal_places=2)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="quotes", db_column="contact_id")
    documents = models.ManyToManyField(Document, related_name="quotes")
    cruise_doctor_first_name = models.CharField(max_length=100, blank=True, null=True)
    cruise_doctor_last_name = models.CharField(max_length=100, blank=True, null=True)
    cruise_line = models.CharField(max_length=100, blank=True, null=True)
    cruise_ship = models.CharField(max_length=100, blank=True, null=True)
    pickup_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="pickup_quotes", db_column="pickup_airport_id")
    dropoff_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="dropoff_quotes", db_column="dropoff_airport_id")
    aircraft_type = models.CharField(max_length=20, choices=[
        ("65", "Learjet 65"),
        ("35", "Learjet 35"),
        ("TBD", "To Be Determined")
    ])
    estimated_flight_time = models.DurationField()
    includes_grounds = models.BooleanField(default=False)
    inquiry_date = models.DateTimeField(default=timezone.now)

    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, blank=True, related_name="quotes", db_column="patient_id")
    lost_reason = models.ForeignKey(LostReason, on_delete=models.SET_NULL, null=True, blank=True, related_name="lost_quotes", db_column="lost_reason_id")
    status = models.CharField(max_length=20, choices=[
        ("pending", "Pending"),
        ("active", "Active"),
        ("completed", "Completed"),
        ("lost", "Lost")
    ], default="pending", db_index=True)
    payment_status = models.CharField(max_length=20, choices=[
        ("pending", "Pending"),
        ("partial", "Partial Paid"),
        ("paid", "Paid")
    ], default="pending")
    number_of_stops = models.PositiveIntegerField(default=0)
    quote_pdf = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True, blank=True, related_name="quote_pdfs", db_column="quote_pdf_id")
    quote_pdf_status = models.CharField(max_length=20, choices=[
        ("created", "Created"),
        ("pending", "Pending"),
        ("modified", "Modified"),
        ("accepted", "Accepted"),
        ("denied", "Denied")
    ], default="created")
    # Legacy PHI fields (will be deprecated after migration)
    quote_pdf_email = models.EmailField()
    medical_team = models.CharField(max_length=20, choices=[
        ("RN/RN", "RN/RN"),
        ("RN/Paramedic", "RN/Paramedic"),
        ("RN/MD", "RN/MD"),
        ("RN/RT", "RN/RT"),
        ("standard", "Standard"),
        ("full", "Full")
    ], null=True, blank=True)

    # HIPAA-compliant encrypted fields
    quote_pdf_email_encrypted = models.TextField(null=True, blank=True, help_text="Encrypted quote PDF email")
    quote_pdf_email_hash = models.CharField(max_length=64, null=True, blank=True, db_index=True, help_text="HMAC hash for email searches")
    medical_team_encrypted = models.TextField(null=True, blank=True, help_text="Encrypted medical team")

    payment_agreement = models.ForeignKey(Agreement, on_delete=models.SET_NULL, null=True, blank=True, related_name="payment_quotes", db_column="payment_agreement_id")
    consent_for_transport = models.ForeignKey(Agreement, on_delete=models.SET_NULL, null=True, blank=True, related_name="consent_quotes", db_column="consent_for_transport_id")
    patient_service_agreement = models.ForeignKey(Agreement, on_delete=models.SET_NULL, null=True, blank=True, related_name="service_quotes", db_column="patient_service_agreement_id")
    transactions = models.ManyToManyField(Transaction, related_name="quotes", blank=True)
    
    def get_total_paid(self):
        """Calculate total amount paid from completed transactions."""
        from django.db import models
        return self.transactions.filter(payment_status='completed').aggregate(
            total=models.Sum('amount'))['total'] or 0
    
    def get_remaining_balance(self):
        """Calculate remaining balance after payments."""
        return self.quoted_amount - self.get_total_paid()
    
    def update_payment_status(self):
        """Update payment status based on total payments received."""
        total_paid = self.get_total_paid()
        if total_paid == 0:
            self.payment_status = 'pending'
        elif total_paid >= self.quoted_amount:
            self.payment_status = 'paid'
        else:
            self.payment_status = 'partial'
        self.save()
    
    def __str__(self):
        return f"Quote {self.id} - {self.quoted_amount} - {self.status}"

    # Helper methods for backward compatibility during migration
    def get_quote_pdf_email(self):
        """Get quote PDF email, preferring encrypted version."""
        if self.quote_pdf_email_encrypted:
            try:
                from .encryption import FieldEncryption
                return FieldEncryption.decrypt(self.quote_pdf_email_encrypted)
            except:
                pass
        return self.quote_pdf_email or ''

    def get_medical_team(self):
        """Get medical team, preferring encrypted version."""
        if self.medical_team_encrypted:
            try:
                from .encryption import FieldEncryption
                return FieldEncryption.decrypt(self.medical_team_encrypted)
            except:
                pass
        return self.medical_team or ''

    class Meta:
        indexes = [
            models.Index(fields=['quote_pdf_email_hash']),
        ]

# Passenger model
class Passenger(BaseModel):
    info = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="passengers")

    # Legacy PHI fields (will be deprecated after migration)
    date_of_birth = models.DateField(blank=True, null=True)
    nationality = models.CharField(max_length=100, blank=True, null=True)
    passport_number = models.CharField(max_length=100, blank=True, null=True)
    passport_expiration_date = models.DateField(blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    # HIPAA-compliant encrypted fields
    date_of_birth_encrypted = models.TextField(null=True, blank=True, help_text="Encrypted date of birth")
    nationality_encrypted = models.TextField(null=True, blank=True, help_text="Encrypted nationality")
    passport_number_encrypted = models.TextField(null=True, blank=True, help_text="Encrypted passport number")
    passport_number_hash = models.CharField(max_length=64, null=True, blank=True, db_index=True, help_text="HMAC hash for passport searches")
    passport_expiration_date_encrypted = models.TextField(null=True, blank=True, help_text="Encrypted passport expiration date")
    contact_number_encrypted = models.TextField(null=True, blank=True, help_text="Encrypted contact number")
    contact_number_hash = models.CharField(max_length=64, null=True, blank=True, db_index=True, help_text="HMAC hash for contact number searches")
    notes_encrypted = models.TextField(null=True, blank=True, help_text="Encrypted notes")

    passport_document = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True, blank=True, related_name="passport_passengers", db_column="passport_document_id")
    passenger_ids = models.ManyToManyField('self', blank=True, symmetrical=False, related_name="related_passengers")

    def __str__(self):
        return f"Passenger: {self.info}"

    # Helper methods for backward compatibility during migration
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

    def get_nationality(self):
        """Get nationality, preferring encrypted version."""
        if self.nationality_encrypted:
            try:
                from .encryption import FieldEncryption
                return FieldEncryption.decrypt(self.nationality_encrypted)
            except:
                pass
        return self.nationality or ''

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

    def get_contact_number(self):
        """Get contact number, preferring encrypted version."""
        if self.contact_number_encrypted:
            try:
                from .encryption import FieldEncryption
                return FieldEncryption.decrypt(self.contact_number_encrypted)
            except:
                pass
        return self.contact_number or ''

    def get_notes(self):
        """Get notes, preferring encrypted version."""
        if self.notes_encrypted:
            try:
                from .encryption import FieldEncryption
                return FieldEncryption.decrypt(self.notes_encrypted)
            except:
                pass
        return self.notes or ''

    class Meta:
        indexes = [
            models.Index(fields=['passport_number_hash']),
            models.Index(fields=['contact_number_hash']),
        ]

# Crew Line model
class CrewLine(BaseModel):
    primary_in_command = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="primary_crew_lines", db_column="primary_in_command_id")
    secondary_in_command = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="secondary_crew_lines", db_column="secondary_in_command_id")
    medic_ids = models.ManyToManyField(Contact, related_name="medic_crew_lines")
    
    def __str__(self):
        return f"Crew: {self.primary_in_command} and {self.secondary_in_command}"

# Trip model
class Trip(BaseModel):
    # Legacy PHI fields (will be deprecated after migration)
    email_chain = models.JSONField(default=list, blank=True)
    notes = models.TextField(blank=True, null=True)

    # HIPAA-compliant encrypted fields
    email_chain_encrypted = models.TextField(null=True, blank=True, help_text="Encrypted email chain")
    notes_encrypted = models.TextField(null=True, blank=True, help_text="Encrypted notes")

    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name="trips", null=True, blank=True, db_column="quote_id")
    type = models.CharField(max_length=20, choices=[
        ("medical", "Medical"),
        ("charter", "Charter"),
        ("part 91", "Part 91"),
        ("other", "Other"),
        ("maintenance", "Maintenance")
    ])
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, blank=True, related_name="trips", db_column="patient_id")
    estimated_departure_time = models.DateTimeField(blank=True, null=True)
    post_flight_duty_time = models.DurationField(blank=True, null=True)
    pre_flight_duty_time = models.DurationField(blank=True, null=True)
    aircraft = models.ForeignKey(Aircraft, on_delete=models.SET_NULL, null=True, blank=True, related_name="trips", db_column="aircraft_id")
    trip_number = models.CharField(max_length=20, unique=True, db_index=True)
    internal_itinerary = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True, blank=True, related_name="internal_itinerary_trips", db_column="internal_itinerary_id")
    customer_itinerary = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True, blank=True, related_name="customer_itinerary_trips", db_column="customer_itinerary_id")
    passengers = models.ManyToManyField(Passenger, related_name="trips", blank=True)

    def __str__(self):
        return f"Trip {self.trip_number} - {self.type}"

    def get_live_flight_status(self):
        """
        Check if this trip has any live flights currently in progress.
        Returns dict with status info or None if no live flights.
        """
        from django.utils import timezone

        now = timezone.now()

        # Find any trip lines where current time is between departure and arrival
        live_legs = self.trip_lines.filter(
            departure_time_utc__lte=now,
            arrival_time_utc__gte=now
        ).select_related('origin_airport', 'destination_airport')

        if not live_legs.exists():
            return None

        # Get the first live leg (there should typically only be one)
        leg = live_legs.first()

        # Calculate flight progress
        total_flight_time = leg.arrival_time_utc - leg.departure_time_utc
        elapsed_time = now - leg.departure_time_utc
        progress_percentage = (elapsed_time.total_seconds() / total_flight_time.total_seconds()) * 100

        # Determine flight phase
        if progress_percentage < 10:
            phase = "departed"
            phase_icon = "🛫"
        elif progress_percentage > 90:
            phase = "approaching"
            phase_icon = "🛬"
        else:
            phase = "enroute"
            phase_icon = "✈️"

        # Calculate remaining time
        remaining_time = leg.arrival_time_utc - now

        return {
            'is_live': True,
            'current_leg': {
                'origin': leg.origin_airport.ident,
                'destination': leg.destination_airport.ident,
                'departure_time_local': leg.departure_time_local,
                'arrival_time_local': leg.arrival_time_local,
            },
            'phase': phase,
            'phase_icon': phase_icon,
            'progress_percentage': round(progress_percentage, 1),
            'remaining_minutes': round(remaining_time.total_seconds() / 60),
        }

    # Helper methods for backward compatibility during migration
    def get_email_chain(self):
        """Get email chain, preferring encrypted version."""
        if self.email_chain_encrypted:
            try:
                from .encryption import FieldEncryption
                import json
                email_chain_str = FieldEncryption.decrypt(self.email_chain_encrypted)
                return json.loads(email_chain_str)
            except:
                pass
        return self.email_chain or []

    def get_notes(self):
        """Get notes, preferring encrypted version."""
        if self.notes_encrypted:
            try:
                from .encryption import FieldEncryption
                return FieldEncryption.decrypt(self.notes_encrypted)
            except:
                pass
        return self.notes or ''

# Trip Line model
class TripLine(BaseModel):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="trip_lines", db_column="trip_id")
    origin_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="origin_trip_lines", db_column="origin_airport_id")
    destination_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="destination_trip_lines", db_column="destination_airport_id")
    crew_line = models.ForeignKey(CrewLine, on_delete=models.SET_NULL, null=True, blank=True, related_name="trip_lines", db_column="crew_line_id")
    departure_fbo = models.ForeignKey(FBO, on_delete=models.SET_NULL, null=True, blank=True, related_name="departure_trip_lines")
    arrival_fbo = models.ForeignKey(FBO, on_delete=models.SET_NULL, null=True, blank=True, related_name="arrival_trip_lines")
    departure_time_local = models.DateTimeField()
    departure_time_utc = models.DateTimeField()
    arrival_time_local = models.DateTimeField()
    arrival_time_utc = models.DateTimeField()
    distance = models.DecimalField(max_digits=10, decimal_places=2)
    flight_time = models.DurationField()
    ground_time = models.DurationField()
    passenger_leg = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Trip Line: {self.origin_airport} to {self.destination_airport}"
    
    class Meta:
        ordering = ['departure_time_utc']


class Staff(BaseModel):
    contact = models.OneToOneField("api.Contact", on_delete=models.CASCADE, related_name="staff")
    active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.contact.first_name} {self.contact.last_name}".strip() or str(self.contact_id)


class StaffRole(BaseModel):
    code = models.CharField(max_length=32, unique=True)   # e.g., 'PIC', 'SIC', 'RN', 'PARAMEDIC'
    name = models.CharField(max_length=64)                # e.g., 'Pilot in Command'

    class Meta:
        indexes = [models.Index(fields=["code"])]

    def __str__(self):
        return self.code


class StaffRoleMembership(BaseModel):
    staff = models.ForeignKey("api.Staff", on_delete=models.CASCADE, related_name="role_memberships")
    role = models.ForeignKey("api.StaffRole", on_delete=models.PROTECT, related_name="memberships")
    start_on = models.DateField(null=True, blank=True)
    end_on = models.DateField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["staff", "role", "start_on", "end_on"],
                name="uniq_staff_role_interval"
            )
        ]


class TripEvent(BaseModel):
    """
    Non-flight timeline items attached to a Trip.
    """
    EVENT_TYPES = [
        ("CREW_CHANGE", "Crew Change"),
        ("OVERNIGHT", "Overnight (New Day)"),
    ]

    trip = models.ForeignKey("api.Trip", on_delete=models.CASCADE, related_name="events")
    airport = models.ForeignKey("api.Airport", on_delete=models.PROTECT, related_name="trip_events")

    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)

    # Start/end timestamps (UTC + local) so you can group by day and show durations
    start_time_local = models.DateTimeField()
    start_time_utc = models.DateTimeField()
    end_time_local = models.DateTimeField(blank=True, null=True)  # required for OVERNIGHT
    end_time_utc = models.DateTimeField(blank=True, null=True)

    # Only used for CREW_CHANGE
    crew_line = models.ForeignKey(
        "api.CrewLine", on_delete=models.SET_NULL, null=True, blank=True, related_name="trip_events"
    )

    notes = models.TextField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["trip", "start_time_utc"]),
            models.Index(fields=["event_type"]),
        ]


class Comment(BaseModel):
    """
    Comments attached to any model instance via a generic foreign key.
    """
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    content_object = GenericForeignKey('content_type', 'object_id')

    text = models.TextField()

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]


class Contract(BaseModel):
    """
    Contract model for managing DocuSeal integration and document signing workflows.
    Extends the existing Agreement functionality with DocuSeal-specific fields.
    """
    CONTRACT_TYPES = [
        ('consent_transport', 'Consent for Transport'),
        ('payment_agreement', 'Air Ambulance Payment Agreement'),
        ('patient_service_agreement', 'Patient Service Agreement'),
    ]
    
    CONTRACT_STATUS = [
        ('draft', 'Draft'),
        ('pending', 'Pending Signature'),
        ('signed', 'Signed'),
        ('completed', 'Completed'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
        ('failed', 'Failed'),
    ]
    
    # Basic contract information
    title = models.CharField(max_length=255)
    contract_type = models.CharField(max_length=30, choices=CONTRACT_TYPES)
    status = models.CharField(max_length=20, choices=CONTRACT_STATUS, default='draft')
    
    # Relationships
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='contracts')
    customer_contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='customer_contracts', null=True, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='patient_contracts', null=True, blank=True)
    
    # DocuSeal integration fields
    docuseal_template_id = models.CharField(max_length=100, blank=True, null=True)
    docuseal_submission_id = models.CharField(max_length=100, blank=True, null=True)
    docuseal_webhook_id = models.CharField(max_length=100, blank=True, null=True)
    
    # Legacy PHI fields (will be deprecated after migration)
    signer_email = models.EmailField()
    signer_name = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    # HIPAA-compliant encrypted fields
    signer_email_encrypted = models.TextField(null=True, blank=True, help_text="Encrypted signer email")
    signer_email_hash = models.CharField(max_length=64, null=True, blank=True, db_index=True, help_text="HMAC hash for email searches")
    signer_name_encrypted = models.TextField(null=True, blank=True, help_text="Encrypted signer name")
    notes_encrypted = models.TextField(null=True, blank=True, help_text="Encrypted notes")

    # Signing details
    date_sent = models.DateTimeField(null=True, blank=True)
    date_signed = models.DateTimeField(null=True, blank=True)
    date_expired = models.DateTimeField(null=True, blank=True)

    # Document storage
    unsigned_document = models.ForeignKey(
        Document,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='unsigned_contracts'
    )
    signed_document = models.ForeignKey(
        Document,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='signed_contracts'
    )

    # Additional metadata
    docuseal_response_data = models.JSONField(default=dict, blank=True)
    
    def __str__(self):
        return f"{self.title} - {self.get_contract_type_display()} ({self.get_status_display()})"

    # Helper methods for backward compatibility during migration
    def get_signer_email(self):
        """Get signer email, preferring encrypted version."""
        if self.signer_email_encrypted:
            try:
                from .encryption import FieldEncryption
                return FieldEncryption.decrypt(self.signer_email_encrypted)
            except:
                pass
        return self.signer_email or ''

    def get_signer_name(self):
        """Get signer name, preferring encrypted version."""
        if self.signer_name_encrypted:
            try:
                from .encryption import FieldEncryption
                return FieldEncryption.decrypt(self.signer_name_encrypted)
            except:
                pass
        return self.signer_name or ''

    def get_notes(self):
        """Get notes, preferring encrypted version."""
        if self.notes_encrypted:
            try:
                from .encryption import FieldEncryption
                return FieldEncryption.decrypt(self.notes_encrypted)
            except:
                pass
        return self.notes or ''

    class Meta:
        indexes = [
            models.Index(fields=['trip', 'contract_type']),
            models.Index(fields=['status']),
            models.Index(fields=['docuseal_submission_id']),
            models.Index(fields=['signer_email_hash']),
        ]
    
    def is_pending_signature(self):
        return self.status == 'pending'
    
    def is_signed(self):
        return self.status in ['signed', 'completed']


# SMS Verification Code model for MFA
class SMSVerificationCode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=20)
    code_hash = models.CharField(max_length=64, null=True, blank=True, help_text="SHA-256 hash of the verification code")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    verified = models.BooleanField(default=False)
    attempts = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['phone_number', 'verified']),
            models.Index(fields=['expires_at']),
        ]

    def __str__(self):
        return f"SMS Code for {self.phone_number} - [HASHED]"

    @classmethod
    def create_code(cls, phone_number, user=None, expires_in_minutes=10):
        """Create a new SMS verification code with secure hash storage."""
        import secrets
        import hashlib
        from django.utils import timezone
        from datetime import timedelta

        # Generate a 6-digit code
        code = f"{secrets.randbelow(900000) + 100000:06d}"

        # Create SHA-256 hash of the code for storage
        code_hash = hashlib.sha256(code.encode()).hexdigest()

        # Set expiration time
        expires_at = timezone.now() + timedelta(minutes=expires_in_minutes)

        # Create the code record
        sms_code = cls.objects.create(
            phone_number=phone_number,
            code_hash=code_hash,
            user=user,
            expires_at=expires_at
        )

        # Return both the code record and the raw code (for sending to user)
        return sms_code, code

    @classmethod
    def verify_code(cls, phone_number, code):
        """Verify a code against stored hash."""
        import hashlib
        from django.utils import timezone

        if not code:
            return None

        # Hash the provided code
        code_hash = hashlib.sha256(code.encode()).hexdigest()

        try:
            # Find the most recent valid code record
            sms_code = cls.objects.filter(
                phone_number=phone_number,
                code_hash=code_hash,
                verified=False,
                expires_at__gt=timezone.now()
            ).first()

            if sms_code and sms_code.can_attempt():
                return sms_code
            return None
        except cls.DoesNotExist:
            return None

    def mark_as_verified(self):
        """Mark this code as verified."""
        self.verified = True
        self.save()

    def increment_attempts(self):
        """Increment the attempt counter."""
        self.attempts += 1
        self.save()

    def is_expired(self):
        return timezone.now() > self.expires_at

    def can_attempt(self):
        return self.attempts < 5 and not self.verified and not self.is_expired()