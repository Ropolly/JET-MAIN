from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils import timezone
from common.models import BaseModel


class Quote(BaseModel):
    """Quote model for flight operations pricing."""
    quoted_amount = models.DecimalField(max_digits=10, decimal_places=2)
    contact = models.ForeignKey('contacts.Contact', on_delete=models.CASCADE, related_name="quotes")
    documents = models.ManyToManyField('documents.Document', related_name="quotes")
    
    # Cruise information
    cruise_doctor_first_name = models.CharField(max_length=100, blank=True, null=True)
    cruise_doctor_last_name = models.CharField(max_length=100, blank=True, null=True)
    cruise_line = models.CharField(max_length=100, blank=True, null=True)
    cruise_ship = models.CharField(max_length=100, blank=True, null=True)
    
    # Flight details
    pickup_airport = models.ForeignKey('airports.Airport', on_delete=models.CASCADE, related_name="pickup_quotes")
    dropoff_airport = models.ForeignKey('airports.Airport', on_delete=models.CASCADE, related_name="dropoff_quotes")
    aircraft_type = models.CharField(max_length=20, choices=[
        ("65", "Learjet 65"),
        ("35", "Learjet 35"),
        ("TBD", "To Be Determined")
    ])
    estimated_flight_time = models.DurationField()
    includes_grounds = models.BooleanField(default=False)
    number_of_stops = models.PositiveIntegerField(default=0)
    
    # Medical team configuration
    medical_team = models.CharField(max_length=20, choices=[
        ("RN/RN", "RN/RN"),
        ("RN/Paramedic", "RN/Paramedic"),
        ("RN/MD", "RN/MD"),
        ("RN/RT", "RN/RT"),
        ("standard", "Standard"),
        ("full", "Full")
    ])
    
    # Status and dates
    inquiry_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=[
        ("pending", "Pending"),
        ("active", "Active"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled")
    ], default="pending", db_index=True)
    
    # Payment information
    payment_status = models.CharField(max_length=20, choices=[
        ("pending", "Pending"),
        ("partial", "Partial Paid"),
        ("paid", "Paid")
    ], default="pending")
    
    # Related entities
    patient = models.ForeignKey('Patient', on_delete=models.SET_NULL, null=True, blank=True, related_name="quotes")
    transactions = models.ManyToManyField('finance.Transaction', related_name="quotes", blank=True)
    
    # Documents
    quote_pdf = models.ForeignKey('documents.Document', on_delete=models.SET_NULL, null=True, blank=True, related_name="quote_pdfs")
    quote_pdf_status = models.CharField(max_length=20, choices=[
        ("created", "Created"),
        ("pending", "Pending"),
        ("modified", "Modified"),
        ("accepted", "Accepted"),
        ("denied", "Denied")
    ], default="created")
    quote_pdf_email = models.EmailField()
    
    # Agreements
    payment_agreement = models.ForeignKey('documents.Agreement', on_delete=models.SET_NULL, null=True, blank=True, related_name="payment_quotes")
    consent_for_transport = models.ForeignKey('documents.Agreement', on_delete=models.SET_NULL, null=True, blank=True, related_name="consent_quotes")
    patient_service_agreement = models.ForeignKey('documents.Agreement', on_delete=models.SET_NULL, null=True, blank=True, related_name="service_quotes")
    
    class Meta:
        indexes = [
            models.Index(fields=['status', 'created_on']),
            models.Index(fields=['payment_status']),
        ]
    
    def __str__(self):
        return f"Quote {self.id} - ${self.quoted_amount} - {self.status}"


class Patient(BaseModel):
    """Patient model for medical transport operations."""
    info = models.ForeignKey('contacts.Contact', on_delete=models.CASCADE, related_name="patients")
    
    # Medical requirements
    bed_at_origin = models.BooleanField(default=False)
    bed_at_destination = models.BooleanField(default=False)
    special_instructions = models.TextField(blank=True, null=True)
    
    # Personal information
    date_of_birth = models.DateField()
    nationality = models.CharField(max_length=100)
    
    # Travel documents
    passport_number = models.CharField(max_length=100)
    passport_expiration_date = models.DateField()
    passport_document = models.ForeignKey('documents.Document', on_delete=models.SET_NULL, null=True, blank=True, related_name="passport_patients")
    letter_of_medical_necessity = models.ForeignKey('documents.Document', on_delete=models.SET_NULL, null=True, blank=True, related_name="medical_necessity_patients")
    
    # Status
    status = models.CharField(max_length=20, choices=[
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("active", "Active"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled")
    ], default="pending", db_index=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['status', 'created_on']),
        ]
    
    def __str__(self):
        return f"Patient: {self.info}"


class Passenger(BaseModel):
    """Passenger model for charter operations."""
    info = models.ForeignKey('contacts.Contact', on_delete=models.CASCADE, related_name="passengers")
    
    # Personal information
    date_of_birth = models.DateField(blank=True, null=True)
    nationality = models.CharField(max_length=100, blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    # Travel documents
    passport_number = models.CharField(max_length=100, blank=True, null=True)
    passport_expiration_date = models.DateField(blank=True, null=True)
    passport_document = models.ForeignKey('documents.Document', on_delete=models.SET_NULL, null=True, blank=True, related_name="passport_passengers")
    
    # Relationships
    passenger_ids = models.ManyToManyField('self', blank=True, symmetrical=False, related_name="related_passengers")
    
    def __str__(self):
        return f"Passenger: {self.info}"


class CrewLine(BaseModel):
    """Crew assignment for flight operations."""
    primary_in_command = models.ForeignKey('contacts.Contact', on_delete=models.CASCADE, related_name="primary_crew_lines")
    secondary_in_command = models.ForeignKey('contacts.Contact', on_delete=models.CASCADE, related_name="secondary_crew_lines")
    medic_ids = models.ManyToManyField('contacts.Contact', related_name="medic_crew_lines")
    
    class Meta:
        indexes = [
            models.Index(fields=['primary_in_command', 'secondary_in_command']),
        ]
    
    def __str__(self):
        return f"Crew: {self.primary_in_command} and {self.secondary_in_command}"


class Trip(BaseModel):
    """Main trip model representing a complete flight operation."""
    
    TRIP_TYPES = [
        ("medical", "Medical"),
        ("charter", "Charter"),
        ("part_91", "Part 91"),
        ("other", "Other"),
        ("maintenance", "Maintenance")
    ]
    
    # Basic information
    trip_number = models.CharField(max_length=20, unique=True, db_index=True)
    type = models.CharField(max_length=20, choices=TRIP_TYPES)
    notes = models.TextField(blank=True, null=True)
    
    # Related entities
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name="trips", null=True, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, blank=True, related_name="trips")
    aircraft = models.ForeignKey('aircraft.Aircraft', on_delete=models.SET_NULL, null=True, blank=True, related_name="trips")
    passengers = models.ManyToManyField(Passenger, related_name="trips", blank=True)
    
    # Timing
    estimated_departure_time = models.DateTimeField(blank=True, null=True)
    pre_flight_duty_time = models.DurationField(blank=True, null=True)
    post_flight_duty_time = models.DurationField(blank=True, null=True)
    
    # Documents
    internal_itinerary = models.ForeignKey('documents.Document', on_delete=models.SET_NULL, null=True, blank=True, related_name="internal_itinerary_trips")
    customer_itinerary = models.ForeignKey('documents.Document', on_delete=models.SET_NULL, null=True, blank=True, related_name="customer_itinerary_trips")
    
    # Communication
    email_chain = models.JSONField(default=list, blank=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['trip_number']),
            models.Index(fields=['type', 'status']),
            models.Index(fields=['estimated_departure_time']),
        ]
    
    def __str__(self):
        return f"Trip {self.trip_number} - {self.type}"


class TripLine(BaseModel):
    """Individual flight leg within a trip."""
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="trip_lines")
    
    # Airports and FBOs
    origin_airport = models.ForeignKey('airports.Airport', on_delete=models.CASCADE, related_name="origin_trip_lines")
    destination_airport = models.ForeignKey('airports.Airport', on_delete=models.CASCADE, related_name="destination_trip_lines")
    departure_fbo = models.ForeignKey('contacts.FBO', on_delete=models.SET_NULL, null=True, blank=True, related_name="departure_trip_lines")
    arrival_fbo = models.ForeignKey('contacts.FBO', on_delete=models.SET_NULL, null=True, blank=True, related_name="arrival_trip_lines")
    
    # Crew
    crew_line = models.ForeignKey(CrewLine, on_delete=models.SET_NULL, null=True, blank=True, related_name="trip_lines")
    
    # Timing (both local and UTC for proper timezone handling)
    departure_time_local = models.DateTimeField()
    departure_time_utc = models.DateTimeField()
    arrival_time_local = models.DateTimeField()
    arrival_time_utc = models.DateTimeField()
    
    # Flight details
    distance = models.DecimalField(max_digits=10, decimal_places=2)
    flight_time = models.DurationField()
    ground_time = models.DurationField()
    passenger_leg = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['departure_time_utc']
        indexes = [
            models.Index(fields=['trip', 'departure_time_utc']),
            models.Index(fields=['origin_airport', 'destination_airport']),
        ]
    
    def __str__(self):
        return f"Trip Line: {self.origin_airport} to {self.destination_airport}"


class TripEvent(BaseModel):
    """Non-flight timeline items attached to a Trip."""
    
    EVENT_TYPES = [
        ("CREW_CHANGE", "Crew Change"),
        ("OVERNIGHT", "Overnight (New Day)"),
    ]
    
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="events")
    airport = models.ForeignKey('airports.Airport', on_delete=models.PROTECT, related_name="trip_events")
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    
    # Start/end timestamps (UTC + local) for proper timezone handling
    start_time_local = models.DateTimeField()
    start_time_utc = models.DateTimeField()
    end_time_local = models.DateTimeField(blank=True, null=True)  # required for OVERNIGHT
    end_time_utc = models.DateTimeField(blank=True, null=True)
    
    # Only used for CREW_CHANGE
    crew_line = models.ForeignKey(CrewLine, on_delete=models.SET_NULL, null=True, blank=True, related_name="trip_events")
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        indexes = [
            models.Index(fields=["trip", "start_time_utc"]),
            models.Index(fields=["event_type"]),
        ]
    
    def __str__(self):
        return f"{self.event_type} at {self.airport} - {self.start_time_local}"
