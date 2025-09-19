"""
HIPAA-compliant encryption utilities and custom Django fields.

This module provides field-level encryption for PHI/PII data using AES-GCM
encryption with external key management integration.
"""

import base64
import hashlib
import hmac
import json
import os
from typing import Optional, Any, Dict, Union
from datetime import date, datetime

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class EncryptionError(Exception):
    """Custom exception for encryption-related errors"""
    pass


class KeyVaultError(Exception):
    """Custom exception for key vault-related errors"""
    pass


class FieldEncryption:
    """
    Core encryption/decryption service for PHI data.
    Uses AES-GCM with 256-bit keys from external key vault.
    """

    # Default key vault settings - will be overridden by actual key vault integration
    DEFAULT_DEK_SIZE = 32  # 256 bits
    DEFAULT_NONCE_SIZE = 12  # 96 bits for GCM

    @classmethod
    def get_encryption_key(cls, key_id: Optional[str] = None) -> bytes:
        """
        Retrieve a Data Encryption Key (DEK) from key vault.

        Args:
            key_id: Optional specific key ID, uses default if None

        Returns:
            32-byte encryption key

        Raises:
            KeyVaultError: If key retrieval fails
        """
        try:
            # Import here to avoid circular imports
            from ..utils.key_vault import get_key_vault_manager

            key_vault = get_key_vault_manager()
            return key_vault.get_encryption_key(key_id or 'default')

        except Exception as e:
            # Fallback for development/testing
            if settings.DEBUG:
                key_material = getattr(settings, 'ENCRYPTION_KEY', None)
                if not key_material:
                    # Generate a deterministic key for development only
                    key_material = hashlib.sha256(b'development-key-do-not-use-in-production').digest()

                if isinstance(key_material, str):
                    # If it's a hex string, decode it
                    if len(key_material) == 64:  # 32 bytes = 64 hex chars
                        key_material = bytes.fromhex(key_material)
                    else:
                        # If it's base64 encoded
                        key_material = base64.b64decode(key_material)

                if len(key_material) != cls.DEFAULT_DEK_SIZE:
                    raise KeyVaultError(f"Invalid key size: {len(key_material)} bytes, expected {cls.DEFAULT_DEK_SIZE}")

                return key_material
            else:
                raise KeyVaultError(f"Failed to retrieve encryption key: {str(e)}")

    @classmethod
    def encrypt(cls, plaintext: str, key_id: Optional[str] = None) -> str:
        """
        Encrypt plaintext using AES-GCM.

        Args:
            plaintext: The data to encrypt
            key_id: Optional key identifier

        Returns:
            Base64-encoded encrypted data with metadata

        Raises:
            EncryptionError: If encryption fails
        """
        if not plaintext:
            return ''

        try:
            # Get encryption key
            key = cls.get_encryption_key(key_id)

            # Generate random nonce
            nonce = os.urandom(cls.DEFAULT_NONCE_SIZE)

            # Encrypt the data
            aesgcm = AESGCM(key)
            ciphertext = aesgcm.encrypt(nonce, plaintext.encode('utf-8'), None)

            # Package the encrypted data with metadata
            encrypted_package = {
                'version': '1.0',
                'algorithm': 'AES-GCM',
                'key_id': key_id or 'default',
                'nonce': base64.b64encode(nonce).decode('ascii'),
                'ciphertext': base64.b64encode(ciphertext).decode('ascii'),
                'timestamp': timezone.now().isoformat()
            }

            # Return base64-encoded JSON package
            package_json = json.dumps(encrypted_package, separators=(',', ':'))
            return base64.b64encode(package_json.encode('utf-8')).decode('ascii')

        except Exception as e:
            raise EncryptionError(f"Encryption failed: {str(e)}")

    @classmethod
    def decrypt(cls, encrypted_data: str) -> str:
        """
        Decrypt data encrypted with encrypt().

        Args:
            encrypted_data: Base64-encoded encrypted package

        Returns:
            Decrypted plaintext

        Raises:
            EncryptionError: If decryption fails
        """
        if not encrypted_data:
            return ''

        try:
            # Decode the package
            package_json = base64.b64decode(encrypted_data).decode('utf-8')
            package = json.loads(package_json)

            # Validate package format
            required_fields = ['version', 'algorithm', 'key_id', 'nonce', 'ciphertext']
            if not all(field in package for field in required_fields):
                raise EncryptionError("Invalid encrypted data format")

            # Check version compatibility
            if package['version'] != '1.0':
                raise EncryptionError(f"Unsupported encryption version: {package['version']}")

            # Check algorithm
            if package['algorithm'] != 'AES-GCM':
                raise EncryptionError(f"Unsupported algorithm: {package['algorithm']}")

            # Get decryption key
            key = cls.get_encryption_key(package['key_id'])

            # Decode nonce and ciphertext
            nonce = base64.b64decode(package['nonce'])
            ciphertext = base64.b64decode(package['ciphertext'])

            # Decrypt
            aesgcm = AESGCM(key)
            plaintext_bytes = aesgcm.decrypt(nonce, ciphertext, None)

            return plaintext_bytes.decode('utf-8')

        except json.JSONDecodeError:
            raise EncryptionError("Invalid encrypted data format: not valid JSON")
        except Exception as e:
            raise EncryptionError(f"Decryption failed: {str(e)}")

    @classmethod
    def generate_search_hash(cls, value: str, salt: Optional[str] = None) -> str:
        """
        Generate HMAC hash for searchable encrypted fields.

        Args:
            value: The value to hash
            salt: Optional salt, uses default if None

        Returns:
            Hex-encoded HMAC hash
        """
        if not value:
            return ''

        # Use configured salt or generate one
        search_salt = salt or getattr(settings, 'SEARCH_SALT', 'default-search-salt-change-in-production')

        if isinstance(search_salt, str):
            search_salt = search_salt.encode('utf-8')

        # Generate HMAC-SHA256 hash
        hmac_hash = hmac.new(
            search_salt,
            value.lower().encode('utf-8'),  # Normalize case for consistent searching
            hashlib.sha256
        ).hexdigest()

        return hmac_hash


class EncryptedFieldMixin:
    """Base mixin for encrypted fields with common functionality."""

    def __init__(self, *args, **kwargs):
        # Remove encryption-specific kwargs before passing to parent
        self.encrypt_blank = kwargs.pop('encrypt_blank', False)
        super().__init__(*args, **kwargs)

    def get_prep_value(self, value):
        """Convert Python object to database storage format."""
        if value is None:
            return None
        if value == '' and not self.encrypt_blank:
            return ''

        # Convert value to string if it isn't already
        if not isinstance(value, str):
            if isinstance(value, date):
                value = value.isoformat()
            else:
                value = str(value)

        try:
            return FieldEncryption.encrypt(value)
        except EncryptionError:
            # Log the error but don't expose details
            if settings.DEBUG:
                raise
            return value  # Fallback to unencrypted in production if encryption fails

    def from_db_value(self, value, expression, connection):
        """Convert database value to Python object."""
        if value is None:
            return None
        if value == '':
            return ''

        try:
            return FieldEncryption.decrypt(value)
        except EncryptionError:
            # If decryption fails, might be legacy unencrypted data
            if settings.DEBUG:
                raise
            return value  # Return as-is, might be legacy data

    def to_python(self, value):
        """Convert value to appropriate Python type."""
        if value is None:
            return None
        if isinstance(value, str):
            return value
        return str(value)


class EncryptedCharField(EncryptedFieldMixin, models.TextField):
    """
    Encrypted CharField for storing short encrypted strings.
    Stores encrypted data as TEXT to accommodate encryption overhead.
    """
    description = "Encrypted character field"

    def __init__(self, max_length=None, **kwargs):
        # Store original max_length for validation but don't pass to TextField
        self.max_length = max_length
        super().__init__(**kwargs)

    def to_python(self, value):
        value = super().to_python(value)
        if value and self.max_length and len(value) > self.max_length:
            raise ValidationError(f'Value too long (max {self.max_length} characters)')
        return value


class EncryptedTextField(EncryptedFieldMixin, models.TextField):
    """Encrypted TextField for storing long encrypted text."""
    description = "Encrypted text field"


class EncryptedEmailField(EncryptedFieldMixin, models.TextField):
    """
    Encrypted email field with automatic search hash generation.
    Creates a companion _hash field for email searches.
    """
    description = "Encrypted email field"

    def contribute_to_class(self, cls, name, **kwargs):
        super().contribute_to_class(cls, name, **kwargs)

        # Add a companion hash field for searches
        hash_field_name = f"{name}_hash"
        if not hasattr(cls, hash_field_name):
            hash_field = models.CharField(
                max_length=64,
                null=True,
                blank=True,
                db_index=True,
                editable=False
            )
            cls.add_to_class(hash_field_name, hash_field)

    def pre_save(self, model_instance, add):
        """Generate search hash before saving."""
        value = super().pre_save(model_instance, add)

        # Generate search hash for the companion field
        hash_field_name = f"{self.name}_hash"
        if hasattr(model_instance, hash_field_name):
            if value:
                hash_value = FieldEncryption.generate_search_hash(value)
                setattr(model_instance, hash_field_name, hash_value)
            else:
                setattr(model_instance, hash_field_name, None)

        return value


class EncryptedDateField(EncryptedFieldMixin, models.TextField):
    """Encrypted date field that stores dates as encrypted ISO strings."""
    description = "Encrypted date field"

    def to_python(self, value):
        """Convert to Python date object."""
        if value is None:
            return None
        if isinstance(value, date):
            return value
        if isinstance(value, str):
            if value == '':
                return None
            try:
                # Try to parse as ISO date string
                return datetime.fromisoformat(value).date()
            except ValueError:
                # Might be encrypted data that needs decryption first
                try:
                    decrypted = FieldEncryption.decrypt(value)
                    return datetime.fromisoformat(decrypted).date()
                except:
                    raise ValidationError(f'Invalid date format: {value}')
        raise ValidationError(f'Invalid date value: {value}')

    def get_prep_value(self, value):
        """Convert date to encrypted ISO string."""
        if value is None:
            return None
        if isinstance(value, date):
            return super().get_prep_value(value.isoformat())
        if isinstance(value, str) and value:
            # Validate it's a proper date string
            try:
                datetime.fromisoformat(value)
                return super().get_prep_value(value)
            except ValueError:
                raise ValidationError(f'Invalid date format: {value}')
        return super().get_prep_value(value)


class SearchableEncryptedField(EncryptedCharField):
    """
    Base class for encrypted fields that need to be searchable.
    Automatically creates a companion _hash field for searches.
    """

    def contribute_to_class(self, cls, name, **kwargs):
        super().contribute_to_class(cls, name, **kwargs)

        # Add a companion hash field for searches
        hash_field_name = f"{name}_hash"
        if not hasattr(cls, hash_field_name):
            hash_field = models.CharField(
                max_length=64,
                null=True,
                blank=True,
                db_index=True,
                editable=False
            )
            cls.add_to_class(hash_field_name, hash_field)

    def pre_save(self, model_instance, add):
        """Generate search hash before saving."""
        value = super().pre_save(model_instance, add)

        # Generate search hash for the companion field
        hash_field_name = f"{self.name}_hash"
        if hasattr(model_instance, hash_field_name):
            if value:
                # Get the decrypted value for hashing
                try:
                    decrypted_value = FieldEncryption.decrypt(value) if value else ''
                    hash_value = FieldEncryption.generate_search_hash(decrypted_value)
                    setattr(model_instance, hash_field_name, hash_value)
                except:
                    # If we can't decrypt, it might be plain text during migration
                    hash_value = FieldEncryption.generate_search_hash(value)
                    setattr(model_instance, hash_field_name, hash_value)
            else:
                setattr(model_instance, hash_field_name, None)

        return value


# Utility functions for working with encrypted fields

def search_encrypted_field(model_class, field_name: str, search_value: str) -> models.QuerySet:
    """
    Search for records with encrypted field matching the given value.

    Args:
        model_class: The Django model class
        field_name: Name of the encrypted field to search
        search_value: Value to search for

    Returns:
        QuerySet of matching records
    """
    if not search_value:
        return model_class.objects.none()

    # Generate hash for the search value
    search_hash = FieldEncryption.generate_search_hash(search_value)

    # Search using the companion hash field
    hash_field_name = f"{field_name}_hash"
    return model_class.objects.filter(**{hash_field_name: search_hash})


def bulk_encrypt_field_data(model_class, field_name: str, batch_size: int = 1000) -> Dict[str, Any]:
    """
    Utility function to encrypt existing plaintext data in a field.
    Used during migration from plaintext to encrypted fields.

    Args:
        model_class: The Django model class
        field_name: Name of the field to encrypt
        batch_size: Number of records to process per batch

    Returns:
        Dictionary with migration statistics
    """
    stats = {
        'total_records': 0,
        'encrypted_records': 0,
        'skipped_records': 0,
        'errors': []
    }

    # Get all records that need encryption
    queryset = model_class.objects.all()
    stats['total_records'] = queryset.count()

    # Process in batches
    for i in range(0, stats['total_records'], batch_size):
        batch = queryset[i:i + batch_size]

        for record in batch:
            try:
                current_value = getattr(record, field_name)
                if current_value:
                    # Try to decrypt first - if it works, it's already encrypted
                    try:
                        FieldEncryption.decrypt(current_value)
                        stats['skipped_records'] += 1
                        continue
                    except EncryptionError:
                        # Not encrypted yet, proceed with encryption
                        pass

                    # Encrypt the value
                    encrypted_value = FieldEncryption.encrypt(current_value)
                    setattr(record, field_name, encrypted_value)
                    record.save(update_fields=[field_name])
                    stats['encrypted_records'] += 1
                else:
                    stats['skipped_records'] += 1

            except Exception as e:
                error_msg = f"Error encrypting record {record.pk}: {str(e)}"
                stats['errors'].append(error_msg)

    return stats