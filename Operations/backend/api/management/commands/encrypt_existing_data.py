"""
Django management command to encrypt existing PHI data for HIPAA compliance.

This command migrates plaintext PHI data to encrypted format using the dual-column
approach for zero-downtime migration.

Usage:
    python manage.py encrypt_existing_data --model=Contact --dry-run
    python manage.py encrypt_existing_data --all-models --batch-size=500
    python manage.py encrypt_existing_data --verify-only
"""

import json
import sys
from typing import Dict, List, Tuple, Any, Type
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from django.db import models, transaction
from django.conf import settings
from django.apps import apps

from api.encryption import FieldEncryption, EncryptionError
from api.models import (
    UserProfile, Contact, Patient, Passenger, Quote, Trip,
    Agreement, Contract, SMSVerificationCode, UserActivationToken
)


class Command(BaseCommand):
    help = 'Encrypt existing PHI data for HIPAA compliance'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stats = {
            'total_processed': 0,
            'successfully_encrypted': 0,
            'already_encrypted': 0,
            'errors': 0,
            'error_details': []
        }

        # Define models and their encrypted fields mapping
        self.MODEL_FIELD_MAPPING = {
            'UserProfile': {
                'model': UserProfile,
                'fields': [
                    ('first_name', 'first_name_encrypted'),
                    ('last_name', 'last_name_encrypted'),
                    ('email', 'email_encrypted'),
                    ('phone', 'phone_encrypted'),
                    ('address_line1', 'address_line1_encrypted'),
                    ('address_line2', 'address_line2_encrypted'),
                    ('city', 'city_encrypted'),
                    ('state', 'state_encrypted'),
                    ('zip', 'zip_encrypted'),
                    ('country', 'country_encrypted'),
                ]
            },
            'Contact': {
                'model': Contact,
                'fields': [
                    ('first_name', 'first_name_encrypted'),
                    ('last_name', 'last_name_encrypted'),
                    ('email', 'email_encrypted'),
                    ('phone', 'phone_encrypted'),
                    ('address_line1', 'address_line1_encrypted'),
                    ('address_line2', 'address_line2_encrypted'),
                    ('city', 'city_encrypted'),
                    ('state', 'state_encrypted'),
                    ('zip', 'zip_encrypted'),
                    ('country', 'country_encrypted'),
                    ('nationality', 'nationality_encrypted'),
                    ('date_of_birth', 'date_of_birth_encrypted'),
                    ('passport_number', 'passport_number_encrypted'),
                    ('passport_expiration_date', 'passport_expiration_date_encrypted'),
                ]
            },
            'Patient': {
                'model': Patient,
                'fields': [
                    ('date_of_birth', 'date_of_birth_encrypted'),
                    ('nationality', 'nationality_encrypted'),
                    ('passport_number', 'passport_number_encrypted'),
                    ('passport_expiration_date', 'passport_expiration_date_encrypted'),
                    ('special_instructions', 'special_instructions_encrypted'),
                ]
            },
            'Passenger': {
                'model': Passenger,
                'fields': [
                    ('date_of_birth', 'date_of_birth_encrypted'),
                    ('nationality', 'nationality_encrypted'),
                    ('passport_number', 'passport_number_encrypted'),
                    ('passport_expiration_date', 'passport_expiration_date_encrypted'),
                    ('contact_number', 'contact_number_encrypted'),
                    ('notes', 'notes_encrypted'),
                ]
            },
            'Quote': {
                'model': Quote,
                'fields': [
                    ('quote_pdf_email', 'quote_pdf_email_encrypted'),
                    ('medical_team', 'medical_team_encrypted'),
                ]
            },
            'Trip': {
                'model': Trip,
                'fields': [
                    ('email_chain', 'email_chain_encrypted'),
                    ('notes', 'notes_encrypted'),
                ]
            },
            'Agreement': {
                'model': Agreement,
                'fields': [
                    ('destination_email', 'destination_email_encrypted'),
                ]
            },
            'Contract': {
                'model': Contract,
                'fields': [
                    ('signer_email', 'signer_email_encrypted'),
                    ('signer_name', 'signer_name_encrypted'),
                    ('notes', 'notes_encrypted'),
                ]
            }
        }

    def add_arguments(self, parser):
        parser.add_argument(
            '--model',
            type=str,
            help='Specific model to encrypt (e.g., Contact, Patient)',
        )
        parser.add_argument(
            '--all-models',
            action='store_true',
            help='Encrypt all models with PHI data',
        )
        parser.add_argument(
            '--batch-size',
            type=int,
            default=1000,
            help='Number of records to process per batch (default: 1000)',
        )
        parser.add_argument(
            '--limit',
            type=int,
            help='Maximum number of records to process (for testing)',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be encrypted without making changes',
        )
        parser.add_argument(
            '--verify-only',
            action='store_true',
            help='Verify existing encrypted data integrity',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force re-encryption of already encrypted data',
        )
        parser.add_argument(
            '--backup-path',
            type=str,
            help='Path to create encrypted backup before migration',
        )

    def handle(self, *args, **options):
        """Main command handler."""

        # Validate arguments
        if not options['all_models'] and not options['model'] and not options['verify_only']:
            raise CommandError("Must specify --model, --all-models, or --verify-only")

        if options['verify_only']:
            self.verify_encrypted_data(options)
            return

        # Create backup if requested
        if options['backup_path']:
            self.create_backup(options['backup_path'], options)

        # Determine which models to process
        if options['all_models']:
            models_to_process = list(self.MODEL_FIELD_MAPPING.keys())
        else:
            model_name = options['model']
            if model_name not in self.MODEL_FIELD_MAPPING:
                raise CommandError(f"Unknown model: {model_name}. Available: {list(self.MODEL_FIELD_MAPPING.keys())}")
            models_to_process = [model_name]

        # Process each model
        for model_name in models_to_process:
            self.stdout.write(f"\n{'-' * 60}")
            self.stdout.write(f"Processing model: {model_name}")
            self.stdout.write(f"{'-' * 60}")

            try:
                self.encrypt_model_data(model_name, options)
            except Exception as e:
                self.stderr.write(f"Error processing {model_name}: {str(e)}")
                self.stats['errors'] += 1
                self.stats['error_details'].append(f"{model_name}: {str(e)}")

        # Print final statistics
        self.print_final_stats()

    def encrypt_model_data(self, model_name: str, options: Dict[str, Any]):
        """Encrypt data for a specific model."""

        model_config = self.MODEL_FIELD_MAPPING[model_name]
        model_class = model_config['model']
        field_mappings = model_config['fields']

        # Get queryset
        queryset = model_class.objects.all()
        if options['limit']:
            queryset = queryset[:options['limit']]

        total_count = queryset.count()
        self.stdout.write(f"Found {total_count} records to process")

        if total_count == 0:
            return

        # Process in batches
        batch_size = options['batch_size']
        processed = 0

        for i in range(0, total_count, batch_size):
            batch_queryset = queryset[i:i + batch_size]
            batch_stats = self.process_batch(batch_queryset, field_mappings, options)

            processed += batch_stats['processed']
            self.stats['total_processed'] += batch_stats['processed']
            self.stats['successfully_encrypted'] += batch_stats['encrypted']
            self.stats['already_encrypted'] += batch_stats['skipped']
            self.stats['errors'] += batch_stats['errors']

            # Progress update
            progress = (processed / total_count) * 100
            self.stdout.write(f"Progress: {processed}/{total_count} ({progress:.1f}%)")

    def process_batch(self, batch_queryset, field_mappings: List[Tuple[str, str]], options: Dict[str, Any]) -> Dict[str, int]:
        """Process a batch of records."""

        batch_stats = {
            'processed': 0,
            'encrypted': 0,
            'skipped': 0,
            'errors': 0
        }

        for record in batch_queryset:
            try:
                record_encrypted = False

                for source_field, target_field in field_mappings:
                    # Check if target field exists (might not in dual-column setup yet)
                    if not hasattr(record, target_field):
                        continue

                    source_value = getattr(record, source_field, None)
                    target_value = getattr(record, target_field, None)

                    # Skip if source is empty
                    if not source_value:
                        continue

                    # Check if already encrypted (unless force flag is set)
                    if target_value and not options['force']:
                        try:
                            # Try to decrypt to see if it's already encrypted
                            FieldEncryption.decrypt(target_value)
                            batch_stats['skipped'] += 1
                            continue
                        except EncryptionError:
                            # Not encrypted yet, proceed
                            pass

                    # Encrypt the data
                    if not options['dry_run']:
                        try:
                            encrypted_value = FieldEncryption.encrypt(str(source_value))
                            setattr(record, target_field, encrypted_value)

                            # Generate search hash if it's a searchable field
                            hash_field = f"{target_field.replace('_encrypted', '')}_hash"
                            if hasattr(record, hash_field):
                                search_hash = FieldEncryption.generate_search_hash(str(source_value))
                                setattr(record, hash_field, search_hash)

                            record_encrypted = True

                        except Exception as e:
                            self.stderr.write(f"Error encrypting {record.pk}.{source_field}: {str(e)}")
                            batch_stats['errors'] += 1
                            continue
                    else:
                        self.stdout.write(f"Would encrypt: {record.pk}.{source_field}")
                        record_encrypted = True

                # Save the record if any field was encrypted
                if record_encrypted and not options['dry_run']:
                    with transaction.atomic():
                        record.save()
                        batch_stats['encrypted'] += 1

                batch_stats['processed'] += 1

            except Exception as e:
                self.stderr.write(f"Error processing record {record.pk}: {str(e)}")
                batch_stats['errors'] += 1
                self.stats['error_details'].append(f"Record {record.pk}: {str(e)}")

        return batch_stats

    def verify_encrypted_data(self, options: Dict[str, Any]):
        """Verify integrity of encrypted data."""

        self.stdout.write("Verifying encrypted data integrity...")

        total_verified = 0
        total_errors = 0

        for model_name, model_config in self.MODEL_FIELD_MAPPING.items():
            model_class = model_config['model']
            field_mappings = model_config['fields']

            self.stdout.write(f"\nVerifying {model_name}...")

            queryset = model_class.objects.all()
            if options['limit']:
                queryset = queryset[:options['limit']]

            for record in queryset:
                for source_field, target_field in field_mappings:
                    if not hasattr(record, target_field):
                        continue

                    source_value = getattr(record, source_field, None)
                    target_value = getattr(record, target_field, None)

                    if not target_value:
                        continue

                    try:
                        # Try to decrypt
                        decrypted_value = FieldEncryption.decrypt(target_value)

                        # Compare with source if both exist
                        if source_value and str(source_value) != decrypted_value:
                            self.stderr.write(
                                f"Mismatch in {model_name} {record.pk}.{source_field}: "
                                f"source='{source_value}' vs decrypted='{decrypted_value}'"
                            )
                            total_errors += 1

                        total_verified += 1

                    except EncryptionError as e:
                        self.stderr.write(
                            f"Decryption failed for {model_name} {record.pk}.{target_field}: {str(e)}"
                        )
                        total_errors += 1

        self.stdout.write(f"\nVerification complete:")
        self.stdout.write(f"  Total fields verified: {total_verified}")
        self.stdout.write(f"  Total errors: {total_errors}")

        if total_errors > 0:
            self.stderr.write(f"❌ Verification failed with {total_errors} errors")
            sys.exit(1)
        else:
            self.stdout.write("✅ All encrypted data verified successfully")

    def create_backup(self, backup_path: str, options: Dict[str, Any]):
        """Create encrypted backup of PHI data before migration."""

        self.stdout.write(f"Creating backup at: {backup_path}")

        backup_data = {
            'created_at': datetime.now().isoformat(),
            'models': {}
        }

        for model_name, model_config in self.MODEL_FIELD_MAPPING.items():
            model_class = model_config['model']
            field_mappings = model_config['fields']

            self.stdout.write(f"Backing up {model_name}...")

            records = []
            for record in model_class.objects.all():
                record_data = {'pk': str(record.pk)}

                for source_field, target_field in field_mappings:
                    source_value = getattr(record, source_field, None)
                    if source_value:
                        # Encrypt for backup
                        encrypted_value = FieldEncryption.encrypt(str(source_value))
                        record_data[source_field] = encrypted_value

                if len(record_data) > 1:  # More than just the PK
                    records.append(record_data)

            backup_data['models'][model_name] = records

        # Save backup
        with open(backup_path, 'w') as f:
            json.dump(backup_data, f, indent=2)

        self.stdout.write(f"✅ Backup created successfully: {backup_path}")

    def print_final_stats(self):
        """Print final migration statistics."""

        self.stdout.write(f"\n{'=' * 60}")
        self.stdout.write("MIGRATION SUMMARY")
        self.stdout.write(f"{'=' * 60}")
        self.stdout.write(f"Total records processed: {self.stats['total_processed']}")
        self.stdout.write(f"Successfully encrypted: {self.stats['successfully_encrypted']}")
        self.stdout.write(f"Already encrypted (skipped): {self.stats['already_encrypted']}")
        self.stdout.write(f"Errors: {self.stats['errors']}")

        if self.stats['errors'] > 0:
            self.stdout.write(f"\nError details:")
            for error in self.stats['error_details']:
                self.stderr.write(f"  - {error}")

        success_rate = 0
        if self.stats['total_processed'] > 0:
            success_rate = (self.stats['successfully_encrypted'] / self.stats['total_processed']) * 100

        self.stdout.write(f"\nSuccess rate: {success_rate:.1f}%")

        if self.stats['errors'] == 0:
            self.stdout.write("✅ Migration completed successfully!")
        else:
            self.stderr.write("❌ Migration completed with errors. Please review the error details above.")
            sys.exit(1)