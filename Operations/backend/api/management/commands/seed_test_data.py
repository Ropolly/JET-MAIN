from django.core.management.base import BaseCommand
from django.utils import timezone
from decimal import Decimal
import random
from datetime import datetime, timedelta
from api.models import (
    Contact, Patient, Quote, Trip, Passenger, Airport, Aircraft, 
    TripLine, CrewLine, Staff, StaffRole
)

class Command(BaseCommand):
    help = 'Seeds the database with test data: 20 patients, quotes, trips, and passengers'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to seed test data...'))
        
        # Get some airports and aircraft for relationships
        airports = list(Airport.objects.all()[:10])
        aircraft = list(Aircraft.objects.all()[:5])
        
        if not airports:
            self.stdout.write(self.style.ERROR('No airports found. Please seed airports first.'))
            return
            
        if not aircraft:
            self.stdout.write(self.style.ERROR('No aircraft found. Please seed aircraft first.'))
            return
        
        # Create staff if they don't exist
        self.create_staff_if_needed()
        staff_members = list(Staff.objects.all()[:10])
        
        # Seed patients
        patients = self.seed_patients()
        self.stdout.write(self.style.SUCCESS(f'Created {len(patients)} patients'))
        
        # Seed passengers
        passengers = self.seed_passengers()
        self.stdout.write(self.style.SUCCESS(f'Created {len(passengers)} passengers'))
        
        # Seed quotes
        quotes = self.seed_quotes(patients, airports)
        self.stdout.write(self.style.SUCCESS(f'Created {len(quotes)} quotes'))
        
        # Seed trips
        trips = self.seed_trips(patients, aircraft, airports, staff_members, quotes)
        self.stdout.write(self.style.SUCCESS(f'Created {len(trips)} trips'))
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded all test data!'))

    def create_staff_if_needed(self):
        """Create some basic staff members if they don't exist"""
        if Staff.objects.count() < 5:
            staff_names = [
                ('John', 'Pilot', 'john.pilot@jeticu.com'),
                ('Sarah', 'Copilot', 'sarah.copilot@jeticu.com'),
                ('Mike', 'Nurse', 'mike.nurse@jeticu.com'),
                ('Lisa', 'Paramedic', 'lisa.paramedic@jeticu.com'),
                ('Dave', 'Captain', 'dave.captain@jeticu.com'),
            ]
            
            for first_name, last_name, email in staff_names:
                if not Contact.objects.filter(email=email).exists():
                    contact = Contact.objects.create(
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                        phone=f'+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}'
                    )
                    Staff.objects.create(contact=contact, active=True)

    def seed_patients(self):
        """Create 20 test patients"""
        patients = []
        first_names = ['John', 'Jane', 'Michael', 'Sarah', 'David', 'Lisa', 'Robert', 'Maria', 'James', 'Jennifer',
                      'William', 'Patricia', 'Richard', 'Linda', 'Joseph', 'Barbara', 'Thomas', 'Elizabeth', 'Daniel', 'Susan']
        last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez',
                     'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin']
        
        for i in range(20):
            # Create contact for patient
            contact = Contact.objects.create(
                first_name=random.choice(first_names),
                last_name=random.choice(last_names),
                email=f'patient{i+1}@example.com',
                phone=f'+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}',
                date_of_birth=datetime.now().date() - timedelta(days=random.randint(365*20, 365*80)),
                nationality='United States'
            )
            
            # Create patient
            patient = Patient.objects.create(
                info=contact,
                date_of_birth=contact.date_of_birth,
                nationality=contact.nationality,
                passport_number=f'P{random.randint(100000000, 999999999)}',
                passport_expiration_date=datetime.now().date() + timedelta(days=random.randint(365, 365*5)),
                bed_at_origin=random.choice([True, False]),
                bed_at_destination=random.choice([True, False]),
                special_instructions=f'Special care instructions for patient {i+1}',
                status='active'
            )
            patients.append(patient)
            
        return patients

    def seed_passengers(self):
        """Create 20 test passengers"""
        passengers = []
        first_names = ['Alex', 'Chris', 'Jordan', 'Taylor', 'Morgan', 'Casey', 'Jamie', 'Riley', 'Avery', 'Quinn',
                      'Sage', 'River', 'Phoenix', 'Skyler', 'Cameron', 'Dakota', 'Emery', 'Finley', 'Harper', 'Kendall']
        last_names = ['White', 'Harris', 'Clark', 'Lewis', 'Robinson', 'Walker', 'Perez', 'Hall', 'Young', 'Allen',
                     'Sanchez', 'Wright', 'King', 'Scott', 'Green', 'Baker', 'Adams', 'Nelson', 'Hill', 'Ramirez']
        
        for i in range(20):
            # Create contact for passenger
            contact = Contact.objects.create(
                first_name=random.choice(first_names),
                last_name=random.choice(last_names),
                email=f'passenger{i+1}@example.com',
                phone=f'+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}',
                date_of_birth=datetime.now().date() - timedelta(days=random.randint(365*18, 365*70))
            )
            
            # Create passenger
            passenger = Passenger.objects.create(
                info=contact,
                date_of_birth=contact.date_of_birth,
                nationality='United States',
                passport_number=f'P{random.randint(100000000, 999999999)}',
                passport_expiration_date=datetime.now().date() + timedelta(days=random.randint(365, 365*5)),
                contact_number=contact.phone,
                notes=f'Passenger notes for {contact.first_name} {contact.last_name}'
            )
            passengers.append(passenger)
            
        return passengers

    def seed_quotes(self, patients, airports):
        """Create 20 test quotes"""
        quotes = []
        
        for i in range(20):
            # Create contact for customer
            contact = Contact.objects.create(
                first_name=f'Customer{i+1}',
                last_name='Family',
                email=f'customer{i+1}@example.com',
                phone=f'+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}'
            )
            
            quote = Quote.objects.create(
                contact=contact,
                patient=random.choice(patients) if random.choice([True, False]) else None,
                pickup_airport=random.choice(airports),
                dropoff_airport=random.choice(airports),
                quoted_amount=Decimal(str(random.randint(5000, 50000))),
                aircraft_type=random.choice(['65', '35', 'TBD']),
                medical_team=random.choice(['RN/RN', 'RN/Paramedic', 'RN/MD', 'standard', 'full']),
                estimated_flight_time=timedelta(hours=random.randint(1, 8)),
                includes_grounds=random.choice([True, False]),
                status=random.choice(['pending', 'active', 'completed', 'cancelled'])
            )
            quotes.append(quote)
            
        return quotes

    def seed_trips(self, patients, aircraft, airports, staff_members, quotes):
        """Create 20 test trips with trip lines"""
        trips = []
        
        for i in range(20):
            # Create trip
            trip = Trip.objects.create(
                trip_number=f'{10000 + i + 1:05d}',
                type=random.choice(['medical', 'charter', 'part 91', 'maintenance']),
                aircraft=random.choice(aircraft) if random.choice([True, False]) else None,
                patient=random.choice(patients) if random.choice([True, False]) else None,
                quote=random.choice(quotes) if random.choice([True, False]) else None,
                status=random.choice(['pending', 'active', 'completed', 'cancelled']),
                notes=f'Trip notes for trip {i+1}',
                estimated_departure_time=timezone.now() + timedelta(days=random.randint(1, 30)),
                pre_flight_duty_time=timedelta(hours=1),
                post_flight_duty_time=timedelta(hours=1)
            )
            
            # Create trip lines for each trip (1-3 legs)
            num_legs = random.randint(1, 3)
            current_time = timezone.now() + timedelta(days=random.randint(1, 30))
            
            for leg in range(num_legs):
                origin = random.choice(airports)
                destination = random.choice([a for a in airports if a != origin])
                
                # Create crew line if we have enough staff
                crew_line = None
                if len(staff_members) >= 2:
                    pic_staff = random.choice(staff_members)
                    sic_staff = random.choice([s for s in staff_members if s != pic_staff])
                    medic_staff = random.sample([s for s in staff_members if s not in [pic_staff, sic_staff]], 
                                              min(2, len(staff_members) - 2))
                    
                    crew_line = CrewLine.objects.create(
                        primary_in_command=pic_staff.contact,
                        secondary_in_command=sic_staff.contact
                    )
                    for medic in medic_staff:
                        crew_line.medic_ids.add(medic.contact)
                
                # Create trip line
                departure_time = current_time + timedelta(hours=random.randint(1, 4))
                flight_duration = timedelta(hours=random.randint(1, 6), minutes=random.randint(0, 59))
                arrival_time = departure_time + flight_duration
                
                TripLine.objects.create(
                    trip=trip,
                    origin_airport=origin,
                    destination_airport=destination,
                    crew_line=crew_line,
                    departure_time_local=departure_time,
                    departure_time_utc=departure_time,
                    arrival_time_local=arrival_time,
                    arrival_time_utc=arrival_time,
                    distance=Decimal(str(random.randint(100, 2000))),
                    flight_time=flight_duration,
                    ground_time=timedelta(hours=1),
                    passenger_leg=True
                )
                
                current_time = arrival_time + timedelta(hours=1)  # 1 hour ground time
            
            trips.append(trip)
            
        return trips