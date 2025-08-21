from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
from api.models import (
    Contact, UserProfile, Role, Department, Airport, Aircraft, 
    Passenger, CrewLine, Trip, TripLine, Quote, Patient, Document, Transaction
)
import os


class Command(BaseCommand):
    help = 'Set up test data for API endpoint testing'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Setting up test data...'))
        
        with transaction.atomic():
            # Create admin user
            admin_user, created = User.objects.get_or_create(
                username='admin',
                defaults={
                    'email': 'admin@jetmain.com',
                    'first_name': 'Admin',
                    'last_name': 'User',
                    'is_staff': True,
                    'is_superuser': True
                }
            )
            if created:
                admin_user.set_password('admin')
                admin_user.save()
                self.stdout.write(f'✅ Created admin user: admin/admin')
            else:
                self.stdout.write(f'✅ Admin user already exists')

            # Create test user
            test_user, created = User.objects.get_or_create(
                username='testuser',
                defaults={
                    'email': 'test@jetmain.com',
                    'first_name': 'Test',
                    'last_name': 'User',
                    'is_staff': False,
                    'is_superuser': False
                }
            )
            if created:
                test_user.set_password('testpass')
                test_user.save()
                self.stdout.write(f'✅ Created test user: testuser/testpass')

            # Create roles
            pilot_role, _ = Role.objects.get_or_create(
                name='Pilot',
                defaults={'description': 'Aircraft pilot'}
            )
            medic_role, _ = Role.objects.get_or_create(
                name='Medic',
                defaults={'description': 'Medical personnel'}
            )
            admin_role, _ = Role.objects.get_or_create(
                name='Admin',
                defaults={'description': 'Administrator'}
            )

            # Create departments
            flight_dept, _ = Department.objects.get_or_create(
                name='Flight Operations',
                defaults={'description': 'Flight operations department'}
            )
            medical_dept, _ = Department.objects.get_or_create(
                name='Medical',
                defaults={'description': 'Medical department'}
            )

            # Create contacts
            contacts = []
            for i in range(1, 6):
                contact, _ = Contact.objects.get_or_create(
                    email=f'contact{i}@jetmain.com',
                    defaults={
                        'first_name': f'Contact{i}',
                        'last_name': f'User{i}',
                        'phone': f'+123456789{i}',
                        'address_line1': f'{i}00 Test Street',
                        'city': 'Test City',
                        'state': 'TS',
                        'zip': f'1234{i}',
                        'country': 'USA'
                    }
                )
                contacts.append(contact)

            # Create UserProfiles
            admin_profile, _ = UserProfile.objects.get_or_create(
                user=admin_user,
                defaults={
                    'first_name': 'Admin',
                    'last_name': 'User',
                    'phone': '+1234567890',
                    'address_line1': '123 Admin Street',
                    'city': 'Admin City',
                    'state': 'AC',
                    'zip': '12345',
                    'country': 'USA'
                }
            )
            admin_profile.roles.add(admin_role)
            admin_profile.departments.add(flight_dept)

            test_profile, _ = UserProfile.objects.get_or_create(
                user=test_user,
                defaults={
                    'first_name': 'Test',
                    'last_name': 'User',
                    'phone': '+1234567891',
                    'address_line1': '456 Test Street',
                    'city': 'Test City',
                    'state': 'TC',
                    'zip': '54321',
                    'country': 'USA'
                }
            )
            test_profile.roles.add(pilot_role)
            test_profile.departments.add(flight_dept)

            # Create airports
            airports = []
            airport_data = [
                ('KORD', 'Chicago O\'Hare', 'Chicago', 'IL'),
                ('KLAX', 'Los Angeles International', 'Los Angeles', 'CA'),
                ('KJFK', 'John F Kennedy International', 'New York', 'NY'),
                ('KDEN', 'Denver International', 'Denver', 'CO')
            ]
            
            for icao, name, city, state in airport_data:
                airport, _ = Airport.objects.get_or_create(
                    icao_code=icao,
                    defaults={
                        'name': name,
                        'city': city,
                        'state': state,
                        'country': 'USA',
                        'latitude': 40.0,
                        'longitude': -87.0
                    }
                )
                airports.append(airport)

            # Create aircraft
            aircraft, _ = Aircraft.objects.get_or_create(
                tail_number='N123JM',
                defaults={
                    'company': 'JET-MAIN',
                    'make': 'Cessna',
                    'model': 'Citation X',
                    'serial_number': 'SN123456',
                    'mgtow': 15000.00
                }
            )

            # Create passengers
            passengers = []
            for i, contact in enumerate(contacts[:3]):
                passenger, _ = Passenger.objects.get_or_create(
                    info=contact,
                    defaults={
                        'passport_number': f'P{i+1}234567',
                        'passport_expiration_date': '2030-12-31',
                        'contact_number': f'+198765432{i+1}',
                        'notes': f'No known allergies for passenger {i+1}',
                        'nationality': 'USA'
                    }
                )
                passengers.append(passenger)

            # Create patients
            patients = []
            for i, contact in enumerate(contacts[3:]):
                patient, _ = Patient.objects.get_or_create(
                    info=contact,
                    defaults={
                        'date_of_birth': '1990-01-01',
                        'nationality': 'USA',
                        'passport_number': f'PT{i+1}234567',
                        'passport_expiration_date': '2030-12-31',
                        'status': 'active',
                        'special_instructions': f'Patient {i+1} medical history',
                        'bed_at_origin': False,
                        'bed_at_destination': False
                    }
                )
                patients.append(patient)

            # Create crew lines
            crew_lines = []
            for i in range(2):
                crew_line, _ = CrewLine.objects.get_or_create(
                    primary_in_command_id=contacts[0],
                    secondary_in_command_id=contacts[1]
                )
                crew_line.medic_ids.add(contacts[2])
                crew_lines.append(crew_line)

            # Create quotes
            quotes = []
            for i in range(2):
                quote, _ = Quote.objects.get_or_create(
                    quoted_amount=15000.00,
                    contact_id=contacts[0],
                    pickup_airport_id=airports[0],
                    dropoff_airport_id=airports[1],
                    defaults={
                        'patient_id': patients[0] if patients else None,
                        'aircraft_type': 'TBD',
                        'estimated_fight_time': 4.0,
                        'medical_team': 'standard',
                        'status': 'pending',
                        'quote_pdf_email': f'quote{i+1}@jetmain.com',
                        'includes_grounds': False,
                        'number_of_stops': 0
                    }
                )
                quotes.append(quote)

            # Create trips
            trips = []
            for i, quote in enumerate(quotes):
                trip, _ = Trip.objects.get_or_create(
                    trip_number=f'TR{i+1:04d}',
                    defaults={
                        'quote_id': quote,
                        'patient_id': patients[0] if patients else None,
                        'aircraft_id': aircraft,
                        'type': 'medical',
                        'estimated_departure_time': '2024-12-01T10:00:00Z'
                    }
                )
                trip.passengers.add(passengers[0])
                trips.append(trip)

            # Create trip lines
            for i, trip in enumerate(trips):
                trip_line, _ = TripLine.objects.get_or_create(
                    trip_id=trip,
                    origin_airport_id=airports[i],
                    destination_airport_id=airports[i+1],
                    defaults={
                        'crew_line_id': crew_lines[0],
                        'departure_time_local': '2024-12-01T10:00:00',
                        'departure_time_utc': '2024-12-01T15:00:00Z',
                        'arrival_time_local': '2024-12-01T14:00:00',
                        'arrival_time_utc': '2024-12-01T19:00:00Z',
                        'distance': 1000.00,
                        'flight_time': 4.0,
                        'ground_time': 1.0,
                        'passenger_leg': True
                    }
                )

            # Create documents
            doc, _ = Document.objects.get_or_create(
                filename='test_document.pdf',
                defaults={
                    'content': b'Test document content',
                    'flag': 0
                }
            )

            # Create transactions
            for i, quote in enumerate(quotes):
                transaction_obj, _ = Transaction.objects.get_or_create(
                    amount=quote.quoted_amount,
                    email=f'transaction{i+1}@jetmain.com',
                    defaults={
                        'payment_method': 'credit_card',
                        'payment_status': 'pending'
                    }
                )

        self.stdout.write(self.style.SUCCESS('✅ Test data setup completed!'))
        self.stdout.write(self.style.SUCCESS(''))
        self.stdout.write(self.style.SUCCESS('Test Accounts:'))
        self.stdout.write(self.style.SUCCESS('  Admin: admin/admin'))
        self.stdout.write(self.style.SUCCESS('  User:  testuser/testpass'))
        self.stdout.write(self.style.SUCCESS(''))
        self.stdout.write(self.style.SUCCESS('You can now run the API tests!'))
