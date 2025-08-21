from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Base model with default fields
class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="%(class)s_created")
    modified_on = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="%(class)s_modified"
    )
    status = models.CharField(max_length=50, default="active")
    lock = models.BooleanField(default=False)
    
    class Meta:
        abstract = True

# Modifications model for tracking changes
class Modification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    model = models.CharField(max_length=100)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    model_key = GenericForeignKey('content_type', 'object_id')
    field = models.CharField(max_length=100)
    before = models.TextField(null=True, blank=True)
    after = models.TextField(null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-time']
        
    def __str__(self):
        return f"{self.model} - {self.field} - {self.time}"

# Permission model
class Permission(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

# Role model
class Role(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    permissions = models.ManyToManyField(Permission, related_name="roles")
    modified_on = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(User, null=True, blank=True,
                                    on_delete=models.SET_NULL,
                                    related_name="%(class)s_modified")
    
    def __str__(self):
        return self.name

# Department model
class Department(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    permission_ids = models.ManyToManyField(Permission, related_name="departments")
    
    def __str__(self):
        return self.name

# Custom User model extending Django's User model
class UserProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    department_ids = models.ManyToManyField(Department, related_name="users")
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address_line1 = models.CharField(max_length=255, blank=True, null=True)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    zip = models.CharField(max_length=20, blank=True, null=True)
    roles = models.ManyToManyField(Role, related_name="users")
    departments = models.ManyToManyField(Department, related_name="department_users")
    flags = models.JSONField(default=list, blank=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# Contact model
class Contact(BaseModel):
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    business_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address_line1 = models.CharField(max_length=255, blank=True, null=True)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zip = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    permission_ids = models.ManyToManyField(Permission, related_name="contacts")
    
    def __str__(self):
        if self.business_name:
            return self.business_name
        return f"{self.first_name} {self.last_name}"
    
    def clean(self):
        if not self.first_name and not self.last_name and not self.business_name:
            raise models.ValidationError("Either first/last name or business name is required")

# FBO (Fixed Base Operator) model
class FBO(BaseModel):
    name = models.CharField(max_length=255)
    address_line1 = models.CharField(max_length=255, blank=True, null=True)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zip = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    contacts = models.ManyToManyField(Contact, related_name="fbos")
    notes = models.TextField(blank=True, null=True)
    permission_ids = models.ManyToManyField(Permission, related_name="fbos")
    
    def __str__(self):
        return self.name

# Ground Transportation model
class Ground(BaseModel):
    name = models.CharField(max_length=255)
    address_line1 = models.CharField(max_length=255, blank=True, null=True)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zip = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    contacts = models.ManyToManyField(Contact, related_name="grounds")
    permission_ids = models.ManyToManyField(Permission, related_name="grounds")
    
    def __str__(self):
        return self.name

# Airport model
class Airport(BaseModel):
    icao_code = models.CharField(max_length=4)
    iata_code = models.CharField(max_length=3)
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100)
    elevation = models.IntegerField(blank=True, null=True)
    fbos = models.ManyToManyField(FBO, related_name="airports", blank=True)
    grounds = models.ManyToManyField(Ground, related_name="airports", blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    timezone = models.CharField(max_length=50)
    permission_ids = models.ManyToManyField(Permission, related_name="airports")
    
    def __str__(self):
        return f"{self.name} ({self.icao_code}/{self.iata_code})"

# Document model (for file storage)
class Document(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    filename = models.CharField(max_length=255)
    content = models.BinaryField()
    flag = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.filename

# Aircraft model
class Aircraft(BaseModel):
    tail_number = models.CharField(max_length=20)
    company = models.CharField(max_length=255)
    mgtow = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Maximum Gross Takeoff Weight")
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.tail_number} - {self.make} {self.model}"

# Transaction model
class Transaction(BaseModel):
    key = models.UUIDField(default=uuid.uuid4, editable=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=[
        ("credit_card", "Credit Card"),
        ("ACH", "ACH Transfer")
    ])
    payment_status = models.CharField(max_length=20, choices=[
        ("created", "Created"),
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("failed", "Failed")
    ], default="created")
    payment_date = models.DateTimeField(default=timezone.now)
    email = models.EmailField()
    
    def __str__(self):
        return f"Transaction {self.key} - {self.amount} - {self.payment_status}"

# Agreement model
class Agreement(BaseModel):
    destination_email = models.EmailField()
    document_unsigned_id = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True, blank=True, related_name="unsigned_agreements")
    document_signed_id = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True, blank=True, related_name="signed_agreements")
    status = models.CharField(max_length=20, choices=[
        ("created", "Created"),
        ("pending", "Pending"),
        ("modified", "Modified"),
        ("signed", "Signed"),
        ("denied", "Denied")
    ], default="created")
    
    def __str__(self):
        return f"Agreement for {self.destination_email} - {self.status}"

# Patient model
class Patient(BaseModel):
    info = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="patients")
    bed_at_origin = models.BooleanField(default=False)
    bed_at_destination = models.BooleanField(default=False)
    date_of_birth = models.DateField()
    nationality = models.CharField(max_length=100)
    passport_number = models.CharField(max_length=100)
    passport_expiration_date = models.DateField()
    passport_document_id = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True, blank=True, related_name="passport_patients")
    special_instructions = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=[
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("active", "Active"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled")
    ], default="pending")
    letter_of_medical_necessity_id = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True, blank=True, related_name="medical_necessity_patients")
    
    def __str__(self):
        return f"Patient: {self.info}"

# Quote model
class Quote(BaseModel):
    quoted_amount = models.DecimalField(max_digits=10, decimal_places=2)
    contact_id = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="quotes")
    documents = models.ManyToManyField(Document, related_name="quotes")
    cruise_doctor_first_name = models.CharField(max_length=100, blank=True, null=True)
    cruise_doctor_last_name = models.CharField(max_length=100, blank=True, null=True)
    cruise_line = models.CharField(max_length=100, blank=True, null=True)
    cruise_ship = models.CharField(max_length=100, blank=True, null=True)
    pickup_airport_id = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="pickup_quotes")
    dropoff_airport_id = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="dropoff_quotes")
    aircraft_type = models.CharField(max_length=20, choices=[
        ("65", "Learjet 65"),
        ("35", "Learjet 35"),
        ("TBD", "To Be Determined")
    ])
    estimated_fight_time = models.DecimalField(max_digits=5, decimal_places=2)
    includes_grounds = models.BooleanField(default=False)
    inquiry_date = models.DateTimeField(default=timezone.now)
    medical_team = models.CharField(max_length=20, choices=[
        ("RN/RN", "RN/RN"),
        ("RN/Paramedic", "RN/Paramedic"),
        ("RN/MD", "RN/MD"),
        ("RN/RT", "RN/RT"),
        ("standard", "Standard"),
        ("full", "Full")
    ])
    patient_first_name = models.CharField(max_length=100, blank=True, null=True)
    patient_last_name = models.CharField(max_length=100, blank=True, null=True)
    patient_id = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, blank=True, related_name="quotes")
    status = models.CharField(max_length=20, choices=[
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("active", "Active"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
        ("paid", "Paid")
    ], default="pending")
    number_of_stops = models.PositiveIntegerField(default=0)
    quote_pdf_id = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True, blank=True, related_name="quote_pdfs")
    quote_pdf_status = models.CharField(max_length=20, choices=[
        ("created", "Created"),
        ("pending", "Pending"),
        ("modified", "Modified"),
        ("accepted", "Accepted"),
        ("denied", "Denied")
    ], default="created")
    quote_pdf_email = models.EmailField()
    payment_agreement_id = models.ForeignKey(Agreement, on_delete=models.SET_NULL, null=True, blank=True, related_name="payment_quotes")
    consent_for_transport_id = models.ForeignKey(Agreement, on_delete=models.SET_NULL, null=True, blank=True, related_name="consent_quotes")
    patient_service_agreement_id = models.ForeignKey(Agreement, on_delete=models.SET_NULL, null=True, blank=True, related_name="service_quotes")
    transactions = models.ManyToManyField(Transaction, related_name="quotes", blank=True)
    
    def __str__(self):
        return f"Quote {self.id} - {self.quoted_amount} - {self.status}"

# Passenger model
class Passenger(BaseModel):
    info = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="passengers")
    date_of_birth = models.DateField(blank=True, null=True)
    nationality = models.CharField(max_length=100, blank=True, null=True)
    passport_number = models.CharField(max_length=100, blank=True, null=True)
    passport_expiration_date = models.DateField(blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    passport_document_id = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True, blank=True, related_name="passport_passengers")
    
    def __str__(self):
        return f"Passenger: {self.info}"

# Crew Line model
class CrewLine(BaseModel):
    primary_in_command_id = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="primary_crew_lines")
    secondary_in_command_id = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="secondary_crew_lines")
    medic_ids = models.ManyToManyField(Contact, related_name="medic_crew_lines")
    
    def __str__(self):
        return f"Crew: {self.primary_in_command_id} and {self.secondary_in_command_id}"

# Trip model
class Trip(BaseModel):
    email_chain = models.JSONField(default=list, blank=True)
    quote_id = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name="trips", null=True, blank=True)
    type = models.CharField(max_length=20, choices=[
        ("medical", "Medical"),
        ("charter", "Charter"),
        ("part 91", "Part 91"),
        ("other", "Other"),
        ("maintenance", "Maintenance")
    ])
    patient_id = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, blank=True, related_name="trips")
    estimated_departure_time = models.DateTimeField(blank=True, null=True)
    post_flight_duty_time = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    pre_flight_duty_time = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    aircraft_id = models.ForeignKey(Aircraft, on_delete=models.SET_NULL, null=True, blank=True, related_name="trips")
    trip_number = models.CharField(max_length=20)
    internal_itinerary_id = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True, blank=True, related_name="internal_itinerary_trips")
    customer_itinerary_id = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True, blank=True, related_name="customer_itinerary_trips")
    passengers = models.ManyToManyField(Passenger, related_name="trips", blank=True)
    
    def __str__(self):
        return f"Trip {self.trip_number} - {self.type}"

# Trip Line model
class TripLine(BaseModel):
    trip_id = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name="trip_lines")
    origin_airport_id = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="origin_trip_lines")
    destination_airport_id = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="destination_trip_lines")
    crew_line_id = models.ForeignKey(CrewLine, on_delete=models.SET_NULL, null=True, blank=True, related_name="trip_lines")
    departure_time_local = models.DateTimeField()
    departure_time_utc = models.DateTimeField()
    arrival_time_local = models.DateTimeField()
    arrival_time_utc = models.DateTimeField()
    distance = models.DecimalField(max_digits=10, decimal_places=2)
    flight_time = models.DecimalField(max_digits=5, decimal_places=2)
    ground_time = models.DecimalField(max_digits=5, decimal_places=2)
    passenger_leg = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Trip Line: {self.origin_airport_id} to {self.destination_airport_id}"
    
    class Meta:
        ordering = ['departure_time_utc']
