from django.core.management.base import BaseCommand
from django.db import transaction
from datetime import datetime, timedelta
from api.models import (
    Contact, Patient, Quote, Trip, Passenger, TripLine, CrewLine
)

class Command(BaseCommand):
    help = 'Removes the test data created by seed_test_data command'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Starting to remove test data...'))
        
        with transaction.atomic():
            # Remove trips with trip numbers 10001-10020
            trips_deleted = Trip.objects.filter(
                trip_number__in=[f'{10000 + i:05d}' for i in range(1, 21)]
            ).delete()
            self.stdout.write(f'Deleted trips: {trips_deleted[0]} records')
            
            # Remove quotes from test customers
            quotes_deleted = Quote.objects.filter(
                contact__email__startswith='customer'
            ).delete()
            self.stdout.write(f'Deleted quotes: {quotes_deleted[0]} records')
            
            # Remove test contacts (customers)
            customer_contacts_deleted = Contact.objects.filter(
                email__startswith='customer'
            ).delete()
            self.stdout.write(f'Deleted customer contacts: {customer_contacts_deleted[0]} records')
            
            # Remove test patients
            patients_deleted = Patient.objects.filter(
                info__email__startswith='patient'
            ).delete()
            self.stdout.write(f'Deleted patients: {patients_deleted[0]} records')
            
            # Remove test patient contacts
            patient_contacts_deleted = Contact.objects.filter(
                email__startswith='patient'
            ).delete()
            self.stdout.write(f'Deleted patient contacts: {patient_contacts_deleted[0]} records')
            
            # Remove test passengers
            passengers_deleted = Passenger.objects.filter(
                info__email__startswith='passenger'
            ).delete()
            self.stdout.write(f'Deleted passengers: {passengers_deleted[0]} records')
            
            # Remove test passenger contacts
            passenger_contacts_deleted = Contact.objects.filter(
                email__startswith='passenger'
            ).delete()
            self.stdout.write(f'Deleted passenger contacts: {passenger_contacts_deleted[0]} records')
            
            # Clean up orphaned crew lines (crew lines not attached to any trip lines)
            orphaned_crew_lines = CrewLine.objects.filter(trip_lines__isnull=True)
            crew_lines_deleted = orphaned_crew_lines.delete()
            self.stdout.write(f'Deleted orphaned crew lines: {crew_lines_deleted[0]} records')
            
        self.stdout.write(self.style.SUCCESS('Successfully removed test data!'))