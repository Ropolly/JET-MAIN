"""
Django management command to test encryption configuration.

Usage:
    python manage.py test_encryption
"""

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from api.models import Contact
from api.encryption import FieldEncryption
import json


class Command(BaseCommand):
    help = 'Test encryption configuration and verify it works correctly'

    def add_arguments(self, parser):
        parser.add_argument(
            '--create-test-contact',
            action='store_true',
            help='Create a test contact to verify encryption works'
        )
        parser.add_argument(
            '--cleanup',
            action='store_true',
            help='Remove test contacts after testing'
        )

    def handle(self, *args, **options):
        self.stdout.write("\n" + "="*60)
        self.stdout.write("ENCRYPTION CONFIGURATION TEST")
        self.stdout.write("="*60 + "\n")

        # 1. Check if ENCRYPTION_KEY is configured
        self.stdout.write("1. Checking ENCRYPTION_KEY configuration...")
        encryption_key = getattr(settings, 'ENCRYPTION_KEY', None)
        if not encryption_key:
            self.stdout.write(self.style.ERROR("   ✗ ENCRYPTION_KEY not found in settings"))
            self.stdout.write(self.style.WARNING("   Please set ENCRYPTION_KEY in your environment variables"))
            return
        else:
            # Don't print the actual key for security
            key_len = len(encryption_key)
            self.stdout.write(self.style.SUCCESS(f"   ✓ ENCRYPTION_KEY found ({key_len} characters)"))

        # 2. Test key retrieval
        self.stdout.write("\n2. Testing encryption key retrieval...")
        try:
            key_bytes = FieldEncryption.get_encryption_key()
            self.stdout.write(self.style.SUCCESS(f"   ✓ Successfully retrieved encryption key ({len(key_bytes)} bytes)"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"   ✗ Failed to retrieve encryption key: {str(e)}"))
            return

        # 3. Test basic encryption/decryption
        self.stdout.write("\n3. Testing basic encryption/decryption...")
        test_data = "Test PHI Data - John Doe"
        try:
            encrypted = FieldEncryption.encrypt(test_data)
            self.stdout.write(self.style.SUCCESS(f"   ✓ Successfully encrypted test data"))

            decrypted = FieldEncryption.decrypt(encrypted)
            if decrypted == test_data:
                self.stdout.write(self.style.SUCCESS(f"   ✓ Successfully decrypted test data"))
            else:
                self.stdout.write(self.style.ERROR(f"   ✗ Decryption failed - data mismatch"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"   ✗ Encryption/decryption failed: {str(e)}"))
            return

        # 4. Test search hash generation
        self.stdout.write("\n4. Testing search hash generation...")
        test_email = "test@example.com"
        try:
            hash1 = FieldEncryption.generate_search_hash(test_email)
            hash2 = FieldEncryption.generate_search_hash(test_email)
            if hash1 == hash2:
                self.stdout.write(self.style.SUCCESS(f"   ✓ Search hash is consistent"))
            else:
                self.stdout.write(self.style.ERROR(f"   ✗ Search hash is not consistent"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"   ✗ Search hash generation failed: {str(e)}"))

        # 5. Test Contact model encryption (if requested)
        if options['create_test_contact']:
            self.stdout.write("\n5. Testing Contact model encryption...")

            test_contact = None
            try:
                # Create a test contact
                test_contact = Contact.objects.create(
                    first_name="Test",
                    last_name="Encryption",
                    email="test.encryption@example.com",
                    phone="+1-555-0123",
                    business_name="Test Encryption Corp"
                )
                self.stdout.write(self.style.SUCCESS(f"   ✓ Created test contact (ID: {test_contact.id})"))

                # Check if fields were encrypted
                if test_contact.first_name_encrypted:
                    self.stdout.write(self.style.SUCCESS(f"   ✓ first_name was encrypted"))
                else:
                    self.stdout.write(self.style.WARNING(f"   ⚠ first_name was NOT encrypted"))

                if test_contact.email_encrypted:
                    self.stdout.write(self.style.SUCCESS(f"   ✓ email was encrypted"))
                else:
                    self.stdout.write(self.style.WARNING(f"   ⚠ email was NOT encrypted"))

                if test_contact.email_hash:
                    self.stdout.write(self.style.SUCCESS(f"   ✓ email search hash was generated"))
                else:
                    self.stdout.write(self.style.WARNING(f"   ⚠ email search hash was NOT generated"))

                # Test retrieval
                retrieved_contact = Contact.objects.get(id=test_contact.id)
                if retrieved_contact.get_first_name() == "Test":
                    self.stdout.write(self.style.SUCCESS(f"   ✓ Decryption works: first_name = '{retrieved_contact.get_first_name()}'"))
                else:
                    self.stdout.write(self.style.ERROR(f"   ✗ Decryption failed for first_name"))

                if retrieved_contact.get_email() == "test.encryption@example.com":
                    self.stdout.write(self.style.SUCCESS(f"   ✓ Decryption works: email = '{retrieved_contact.get_email()}'"))
                else:
                    self.stdout.write(self.style.ERROR(f"   ✗ Decryption failed for email"))

                # Cleanup if requested
                if options['cleanup'] and test_contact:
                    test_contact.delete()
                    self.stdout.write(self.style.SUCCESS(f"   ✓ Cleaned up test contact"))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"   ✗ Contact encryption test failed: {str(e)}"))
                if test_contact and options['cleanup']:
                    test_contact.delete()

        # Summary
        self.stdout.write("\n" + "="*60)
        self.stdout.write("TEST COMPLETE")
        self.stdout.write("="*60)

        # Provide helpful next steps
        self.stdout.write("\n" + self.style.NOTICE("Next steps:"))
        self.stdout.write("1. If encryption is working, run seeders to populate data")
        self.stdout.write("   python manage.py seed_dev")
        self.stdout.write("   python manage.py seed_staff")
        self.stdout.write("2. Test API endpoints to ensure encryption works end-to-end")
        self.stdout.write("3. Monitor logs for any encryption warnings")