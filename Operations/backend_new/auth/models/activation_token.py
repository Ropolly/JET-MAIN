from core.models import BaseModel
from django.contrib.auth.models import User
from django.db import models


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