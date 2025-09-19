"""
External Key Management Service Integration for HIPAA Compliance.

This module provides integration with external key vaults (Azure Key Vault, AWS KMS, etc.)
for secure encryption key management with rotation and audit capabilities.
"""

import base64
import hashlib
import os
import time
from abc import ABC, abstractmethod
from typing import Dict, Optional, Tuple, Any
from datetime import datetime, timedelta
from threading import Lock

from django.conf import settings
from django.core.cache import cache
from django.utils import timezone


class KeyVaultError(Exception):
    """Exception raised for key vault operation errors."""
    pass


class KeyRotationRequired(KeyVaultError):
    """Exception raised when key rotation is required."""
    pass


class BaseKeyVault(ABC):
    """Abstract base class for key vault implementations."""

    @abstractmethod
    def get_key(self, key_id: str) -> bytes:
        """Retrieve a key from the vault."""
        pass

    @abstractmethod
    def create_key(self, key_id: str, key_size: int = 32) -> bytes:
        """Create a new key in the vault."""
        pass

    @abstractmethod
    def rotate_key(self, key_id: str) -> Tuple[bytes, str]:
        """Rotate an existing key, returning new key and version."""
        pass

    @abstractmethod
    def list_keys(self) -> Dict[str, Dict[str, Any]]:
        """List all keys with metadata."""
        pass


class DevelopmentKeyVault(BaseKeyVault):
    """
    Development-only key vault using environment variables.
    WARNING: Only for development/testing - never use in production!
    """

    def __init__(self):
        if not settings.DEBUG:
            raise KeyVaultError("DevelopmentKeyVault can only be used in DEBUG mode")

    def get_key(self, key_id: str) -> bytes:
        """Get a development key (deterministic for consistency)."""
        # Create a deterministic key based on key_id for development
        key_material = hashlib.sha256(f"dev-key-{key_id}".encode()).digest()
        return key_material

    def create_key(self, key_id: str, key_size: int = 32) -> bytes:
        """Create a new development key."""
        return self.get_key(key_id)

    def rotate_key(self, key_id: str) -> Tuple[bytes, str]:
        """Simulate key rotation for development."""
        timestamp = str(int(time.time()))
        new_key = hashlib.sha256(f"dev-key-{key_id}-{timestamp}".encode()).digest()
        return new_key, timestamp

    def list_keys(self) -> Dict[str, Dict[str, Any]]:
        """List development keys."""
        return {
            "default": {
                "created": datetime.now().isoformat(),
                "version": "dev-1",
                "status": "active"
            }
        }


class AzureKeyVault(BaseKeyVault):
    """
    Azure Key Vault integration for production use.
    Requires azure-keyvault-secrets package.
    """

    def __init__(self, vault_url: str, credential=None):
        """
        Initialize Azure Key Vault client.

        Args:
            vault_url: Azure Key Vault URL
            credential: Azure credential (DefaultAzureCredential if None)
        """
        try:
            from azure.keyvault.secrets import SecretClient
            from azure.identity import DefaultAzureCredential
        except ImportError:
            raise KeyVaultError("azure-keyvault-secrets and azure-identity packages required for Azure Key Vault")

        self.vault_url = vault_url
        self.credential = credential or DefaultAzureCredential()
        self.client = SecretClient(vault_url=vault_url, credential=self.credential)

    def get_key(self, key_id: str) -> bytes:
        """Retrieve key from Azure Key Vault."""
        try:
            secret = self.client.get_secret(key_id)
            return base64.b64decode(secret.value)
        except Exception as e:
            raise KeyVaultError(f"Failed to retrieve key {key_id}: {str(e)}")

    def create_key(self, key_id: str, key_size: int = 32) -> bytes:
        """Create a new key in Azure Key Vault."""
        try:
            # Generate random key
            key_bytes = os.urandom(key_size)
            key_b64 = base64.b64encode(key_bytes).decode('ascii')

            # Store in vault
            self.client.set_secret(key_id, key_b64)
            return key_bytes
        except Exception as e:
            raise KeyVaultError(f"Failed to create key {key_id}: {str(e)}")

    def rotate_key(self, key_id: str) -> Tuple[bytes, str]:
        """Rotate key in Azure Key Vault."""
        try:
            # Create new key version
            new_key = os.urandom(32)
            key_b64 = base64.b64encode(new_key).decode('ascii')

            # Update secret (creates new version)
            secret = self.client.set_secret(key_id, key_b64)
            return new_key, secret.properties.version
        except Exception as e:
            raise KeyVaultError(f"Failed to rotate key {key_id}: {str(e)}")

    def list_keys(self) -> Dict[str, Dict[str, Any]]:
        """List all keys in Azure Key Vault."""
        try:
            keys = {}
            for secret_properties in self.client.list_properties_of_secrets():
                keys[secret_properties.name] = {
                    "created": secret_properties.created_on.isoformat() if secret_properties.created_on else None,
                    "updated": secret_properties.updated_on.isoformat() if secret_properties.updated_on else None,
                    "version": secret_properties.version,
                    "enabled": secret_properties.enabled,
                    "expires": secret_properties.expires_on.isoformat() if secret_properties.expires_on else None
                }
            return keys
        except Exception as e:
            raise KeyVaultError(f"Failed to list keys: {str(e)}")


class AWSKeyVault(BaseKeyVault):
    """
    AWS KMS integration for production use.
    Requires boto3 package.
    """

    def __init__(self, region_name: str = 'us-east-1'):
        """Initialize AWS KMS client."""
        try:
            import boto3
        except ImportError:
            raise KeyVaultError("boto3 package required for AWS KMS")

        self.kms_client = boto3.client('kms', region_name=region_name)
        self.region_name = region_name

    def get_key(self, key_id: str) -> bytes:
        """Retrieve key from AWS KMS."""
        try:
            # In AWS KMS, we generate data keys on demand
            response = self.kms_client.generate_data_key(
                KeyId=key_id,
                KeySpec='AES_256'
            )
            return response['Plaintext']
        except Exception as e:
            raise KeyVaultError(f"Failed to retrieve key {key_id}: {str(e)}")

    def create_key(self, key_id: str, key_size: int = 32) -> bytes:
        """Create a new key in AWS KMS."""
        try:
            # Create a new KMS key
            response = self.kms_client.create_key(
                Description=f'Data encryption key for {key_id}',
                Usage='ENCRYPT_DECRYPT'
            )
            key_id = response['KeyMetadata']['KeyId']

            # Generate data key
            data_key_response = self.kms_client.generate_data_key(
                KeyId=key_id,
                KeySpec='AES_256'
            )
            return data_key_response['Plaintext']
        except Exception as e:
            raise KeyVaultError(f"Failed to create key {key_id}: {str(e)}")

    def rotate_key(self, key_id: str) -> Tuple[bytes, str]:
        """Rotate key in AWS KMS."""
        try:
            # Enable automatic key rotation
            self.kms_client.enable_key_rotation(KeyId=key_id)

            # Generate new data key
            response = self.kms_client.generate_data_key(
                KeyId=key_id,
                KeySpec='AES_256'
            )
            return response['Plaintext'], str(int(time.time()))
        except Exception as e:
            raise KeyVaultError(f"Failed to rotate key {key_id}: {str(e)}")

    def list_keys(self) -> Dict[str, Dict[str, Any]]:
        """List all keys in AWS KMS."""
        try:
            keys = {}
            response = self.kms_client.list_keys()

            for key_info in response['Keys']:
                key_id = key_info['KeyId']
                metadata = self.kms_client.describe_key(KeyId=key_id)['KeyMetadata']

                keys[key_id] = {
                    "created": metadata['CreationDate'].isoformat(),
                    "description": metadata.get('Description', ''),
                    "usage": metadata['KeyUsage'],
                    "state": metadata['KeyState'],
                    "arn": metadata['Arn']
                }
            return keys
        except Exception as e:
            raise KeyVaultError(f"Failed to list keys: {str(e)}")


class KeyVaultManager:
    """
    Main interface for key vault operations with caching and rotation.
    """

    def __init__(self):
        self.vault = self._initialize_vault()
        self.cache_ttl = getattr(settings, 'KEY_CACHE_TTL', 3600)  # 1 hour default
        self.rotation_interval = getattr(settings, 'KEY_ROTATION_INTERVAL', 86400 * 30)  # 30 days
        self._lock = Lock()

    def _initialize_vault(self) -> BaseKeyVault:
        """Initialize the appropriate key vault based on configuration."""
        vault_type = getattr(settings, 'KEY_VAULT_TYPE', 'development')

        if vault_type == 'development':
            return DevelopmentKeyVault()
        elif vault_type == 'azure':
            vault_url = getattr(settings, 'AZURE_KEY_VAULT_URL', None)
            if not vault_url:
                raise KeyVaultError("AZURE_KEY_VAULT_URL setting required for Azure Key Vault")
            return AzureKeyVault(vault_url)
        elif vault_type == 'aws':
            region = getattr(settings, 'AWS_REGION', 'us-east-1')
            return AWSKeyVault(region)
        else:
            raise KeyVaultError(f"Unsupported key vault type: {vault_type}")

    def get_encryption_key(self, key_id: str = 'default') -> bytes:
        """
        Get encryption key with caching and rotation check.

        Args:
            key_id: Key identifier

        Returns:
            32-byte encryption key

        Raises:
            KeyVaultError: If key retrieval fails
            KeyRotationRequired: If key rotation is needed
        """
        cache_key = f"encryption_key_{key_id}"

        # Try to get from cache first
        cached_key = cache.get(cache_key)
        if cached_key:
            # Check if rotation is needed
            if self._is_rotation_needed(key_id):
                raise KeyRotationRequired(f"Key {key_id} requires rotation")
            return cached_key

        # Get from vault with lock to prevent concurrent requests
        with self._lock:
            # Double-check cache after acquiring lock
            cached_key = cache.get(cache_key)
            if cached_key:
                return cached_key

            try:
                key = self.vault.get_key(key_id)

                # Cache the key
                cache.set(cache_key, key, self.cache_ttl)

                # Update last access time
                self._update_key_metadata(key_id)

                return key
            except Exception as e:
                raise KeyVaultError(f"Failed to get encryption key: {str(e)}")

    def rotate_key(self, key_id: str = 'default') -> bool:
        """
        Rotate encryption key.

        Args:
            key_id: Key identifier

        Returns:
            True if rotation successful

        Raises:
            KeyVaultError: If rotation fails
        """
        try:
            with self._lock:
                # Rotate in vault
                new_key, version = self.vault.rotate_key(key_id)

                # Update cache
                cache_key = f"encryption_key_{key_id}"
                cache.set(cache_key, new_key, self.cache_ttl)

                # Update metadata
                self._update_key_metadata(key_id, version=version, rotated=True)

                return True
        except Exception as e:
            raise KeyVaultError(f"Key rotation failed: {str(e)}")

    def _is_rotation_needed(self, key_id: str) -> bool:
        """Check if key rotation is needed based on age and usage."""
        metadata_key = f"key_metadata_{key_id}"
        metadata = cache.get(metadata_key, {})

        last_rotation = metadata.get('last_rotation')
        if not last_rotation:
            return True  # No rotation record, assume rotation needed

        # Check if rotation interval has passed
        rotation_time = datetime.fromisoformat(last_rotation)
        if (timezone.now() - rotation_time).total_seconds() > self.rotation_interval:
            return True

        return False

    def _update_key_metadata(self, key_id: str, version: Optional[str] = None, rotated: bool = False):
        """Update key metadata in cache."""
        metadata_key = f"key_metadata_{key_id}"
        metadata = cache.get(metadata_key, {})

        metadata['last_access'] = timezone.now().isoformat()

        if version:
            metadata['version'] = version

        if rotated:
            metadata['last_rotation'] = timezone.now().isoformat()

        # Cache metadata for longer than keys
        cache.set(metadata_key, metadata, self.cache_ttl * 24)

    def health_check(self) -> Dict[str, Any]:
        """Perform health check on key vault connectivity."""
        try:
            # Try to list keys as a connectivity test
            keys = self.vault.list_keys()
            return {
                'status': 'healthy',
                'vault_type': type(self.vault).__name__,
                'key_count': len(keys),
                'timestamp': timezone.now().isoformat()
            }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'error': str(e),
                'vault_type': type(self.vault).__name__,
                'timestamp': timezone.now().isoformat()
            }

    def audit_key_usage(self, key_id: str = 'default') -> Dict[str, Any]:
        """Get audit information for key usage."""
        metadata_key = f"key_metadata_{key_id}"
        metadata = cache.get(metadata_key, {})

        return {
            'key_id': key_id,
            'last_access': metadata.get('last_access'),
            'last_rotation': metadata.get('last_rotation'),
            'version': metadata.get('version'),
            'rotation_needed': self._is_rotation_needed(key_id)
        }


# Global key vault manager instance
_key_vault_manager = None


def get_key_vault_manager() -> KeyVaultManager:
    """Get the global key vault manager instance."""
    global _key_vault_manager
    if _key_vault_manager is None:
        _key_vault_manager = KeyVaultManager()
    return _key_vault_manager


# Convenience functions for common operations

def get_encryption_key(key_id: str = 'default') -> bytes:
    """Get encryption key - convenience function."""
    return get_key_vault_manager().get_encryption_key(key_id)


def rotate_encryption_key(key_id: str = 'default') -> bool:
    """Rotate encryption key - convenience function."""
    return get_key_vault_manager().rotate_key(key_id)


def key_vault_health_check() -> Dict[str, Any]:
    """Check key vault health - convenience function."""
    return get_key_vault_manager().health_check()