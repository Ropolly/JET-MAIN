from django.core.management.base import BaseCommand
from django.db import transaction
from api.models import Trip, TripNumberSequence
import re


class Command(BaseCommand):
    help = 'Normalize existing trip numbers to 5-digit format for immigration compliance'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be changed without making actual changes',
        )
        parser.add_argument(
            '--fix-drafts',
            action='store_true',
            help='Convert existing DRAFT numbers to real sequential numbers',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        fix_drafts = options['fix_drafts']

        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No changes will be made'))

        # Step 1: Normalize numeric trip numbers to 5-digit format
        self.normalize_numeric_trip_numbers(dry_run)

        # Step 2: Optionally convert DRAFT numbers to real numbers
        if fix_drafts:
            self.convert_draft_numbers(dry_run)

        # Step 3: Update sequence to match highest existing number
        self.update_sequence(dry_run)

        self.stdout.write(self.style.SUCCESS('Trip number normalization completed!'))

    def normalize_numeric_trip_numbers(self, dry_run):
        """
        Normalize existing numeric trip numbers to 5-digit format.
        """
        self.stdout.write('\n1. Normalizing numeric trip numbers to 5-digit format...')

        trips_to_update = []

        for trip in Trip.objects.all():
            if trip.trip_number and not trip.trip_number.startswith('DRAFT'):
                # Extract numeric part
                match = re.search(r'\d+', trip.trip_number)
                if match:
                    try:
                        num = int(match.group())
                        normalized = str(num).zfill(5)

                        # Only update if it's different
                        if trip.trip_number != normalized:
                            trips_to_update.append({
                                'trip': trip,
                                'old': trip.trip_number,
                                'new': normalized
                            })
                    except ValueError:
                        self.stdout.write(
                            self.style.WARNING(
                                f'  Could not parse trip number: {trip.trip_number} (Trip ID: {trip.id})'
                            )
                        )

        if trips_to_update:
            self.stdout.write(f'  Found {len(trips_to_update)} trips to normalize:')
            for update in trips_to_update:
                self.stdout.write(f'    {update["old"]} -> {update["new"]} (Trip ID: {update["trip"].id})')

            if not dry_run:
                with transaction.atomic():
                    for update in trips_to_update:
                        update['trip'].trip_number = update['new']
                        update['trip'].save()
                self.stdout.write(self.style.SUCCESS(f'  Updated {len(trips_to_update)} trip numbers'))
        else:
            self.stdout.write('  No trip numbers need normalization')

    def convert_draft_numbers(self, dry_run):
        """
        Convert DRAFT trip numbers to real sequential numbers.
        """
        self.stdout.write('\n2. Converting DRAFT numbers to real sequential numbers...')

        draft_trips = Trip.objects.filter(trip_number__startswith='DRAFT').order_by('created_on')

        if draft_trips.exists():
            self.stdout.write(f'  Found {draft_trips.count()} DRAFT trips to convert:')

            if not dry_run:
                with transaction.atomic():
                    for trip in draft_trips:
                        old_number = trip.trip_number
                        trip.assign_real_trip_number()  # Use the model method
                        self.stdout.write(f'    {old_number} -> {trip.trip_number} (Trip ID: {trip.id})')
            else:
                for trip in draft_trips:
                    self.stdout.write(f'    {trip.trip_number} -> [would get next sequential number] (Trip ID: {trip.id})')
        else:
            self.stdout.write('  No DRAFT trips found')

    def update_sequence(self, dry_run):
        """
        Update the sequence to match the highest existing numeric trip number.
        """
        self.stdout.write('\n3. Updating trip number sequence...')

        # Find the highest numeric trip number
        max_numeric = 0

        for trip in Trip.objects.all():
            if trip.trip_number and not trip.trip_number.startswith('DRAFT'):
                match = re.search(r'\d+', trip.trip_number)
                if match:
                    try:
                        num = int(match.group())
                        max_numeric = max(max_numeric, num)
                    except ValueError:
                        continue

        self.stdout.write(f'  Highest existing trip number: {max_numeric}')

        if not dry_run:
            with transaction.atomic():
                sequence, created = TripNumberSequence.objects.get_or_create(
                    id=1,
                    defaults={'current_number': max_numeric}
                )

                if not created and sequence.current_number != max_numeric:
                    old_number = sequence.current_number
                    sequence.current_number = max_numeric
                    sequence.save()
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'  Updated sequence from {old_number} to {max_numeric}'
                        )
                    )
                else:
                    self.stdout.write('  Sequence is already up to date')
        else:
            current_sequence = TripNumberSequence.objects.filter(id=1).first()
            if current_sequence:
                if current_sequence.current_number != max_numeric:
                    self.stdout.write(f'  Would update sequence from {current_sequence.current_number} to {max_numeric}')
                else:
                    self.stdout.write('  Sequence would remain unchanged')
            else:
                self.stdout.write(f'  Would create sequence with current_number={max_numeric}')

    def validate_trip_numbers(self):
        """
        Validate that all trip numbers follow the correct format.
        """
        self.stdout.write('\n4. Validating trip number formats...')

        invalid_trips = []

        for trip in Trip.objects.all():
            if trip.trip_number:
                # Allow DRAFT numbers or 5-digit numbers
                if not (trip.trip_number.startswith('DRAFT') or
                       re.match(r'^\d{5}$', trip.trip_number)):
                    invalid_trips.append(trip)

        if invalid_trips:
            self.stdout.write(self.style.ERROR(f'  Found {len(invalid_trips)} trips with invalid formats:'))
            for trip in invalid_trips:
                self.stdout.write(f'    Trip ID {trip.id}: "{trip.trip_number}"')
        else:
            self.stdout.write(self.style.SUCCESS('  All trip numbers have valid formats'))

        return len(invalid_trips) == 0