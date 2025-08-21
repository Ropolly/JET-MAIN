from rest_framework import serializers
from .models import (
    Modification, Permission, Role, Department, UserProfile, Contact, 
    FBO, Ground, Airport, Document, Aircraft, Transaction, Agreement,
    Patient, Quote, Passenger, CrewLine, Trip, TripLine
)
from django.contrib.auth.models import User

# User serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff']

# Base serializers
class ModificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modification
        fields = ['id', 'created_on', 'created_by', 'modified_on', 'modified_by']

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'description', 'created_on', 'created_by', 'modified_on', 'modified_by']

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'description', 'permissions', 'created_on', 'created_by', 'status', 'lock']

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'description', 'created_on', 'created_by', 'status', 'lock']

# Contact and location serializers
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'first_name', 'last_name', 'business_name', 'email', 'phone', 
                 'address_line1', 'address_line2', 'city', 'state', 'zip', 'country', 
                 'created_on', 'created_by', 'modified_on', 'modified_by']

class FBOSerializer(serializers.ModelSerializer):
    class Meta:
        model = FBO
        fields = ['id', 'name', 'created_on', 'created_by', 'modified_on', 'modified_by']

class GroundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ground
        fields = ['id', 'name', 'address_line1', 'address_line2', 'city', 'state', 'zip', 
                 'country', 'notes', 'contacts', 'created_on', 'created_by', 
                 'modified_on', 'modified_by']

class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ['id', 'icao_code', 'iata_code', 'name', 'city', 'state', 'country', 
                 'elevation', 'fbos', 'grounds', 'latitude', 'longitude', 'timezone', 
                 'created_on', 'created_by', 'modified_on', 'modified_by']

# Aircraft serializer
class AircraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aircraft
        fields = ['id', 'tail_number', 'company', 'mgtow', 'make', 'model', 'serial_number', 
                 'created_on', 'created_by', 'modified_on', 'modified_by']

# Document serializer (basic for references)
class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'filename', 'flag', 'created_on']

# Agreement serializer
class AgreementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agreement
        fields = ['id', 'destination_email', 'document_unsigned', 'document_signed', 
                 'status', 'created_on', 'created_by', 'modified_on', 'modified_by']

# ========== STANDARDIZED CRUD SERIALIZERS ==========

# 1) User Profiles
class UserProfileReadSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    roles = RoleSerializer(many=True, read_only=True)
    departments = DepartmentSerializer(many=True, read_only=True)
    
    class Meta:
        model = UserProfile
        fields = [
            'id', 'user', 'first_name', 'last_name', 'email', 'phone',
            'address_line1', 'address_line2', 'city', 'state', 'country', 'zip',
            'roles', 'departments', 'flags', 'status', 'created_on'
        ]

class UserProfileWriteSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(
        source='user', queryset=User.objects.all(), write_only=True
    )
    role_ids = serializers.PrimaryKeyRelatedField(
        source='roles', queryset=Role.objects.all(), many=True, write_only=True
    )
    department_ids = serializers.PrimaryKeyRelatedField(
        source='departments', queryset=Department.objects.all(), many=True, write_only=True
    )
    
    class Meta:
        model = UserProfile
        fields = [
            'user_id', 'first_name', 'last_name', 'email', 'phone',
            'address_line1', 'address_line2', 'city', 'state', 'country', 'zip',
            'role_ids', 'department_ids', 'flags', 'status'
        ]

# 2) Passengers
class PassengerReadSerializer(serializers.ModelSerializer):
    info = ContactSerializer(read_only=True)
    passport_document = DocumentSerializer(read_only=True)
    
    class Meta:
        model = Passenger
        fields = [
            'id', 'info', 'date_of_birth', 'nationality', 'passport_number',
            'passport_expiration_date', 'contact_number', 'notes', 'passport_document',
            'status', 'created_on'
        ]

class PassengerWriteSerializer(serializers.ModelSerializer):
    info = serializers.PrimaryKeyRelatedField(
        queryset=Contact.objects.all(), write_only=True
    )
    passport_document = serializers.PrimaryKeyRelatedField(
        queryset=Document.objects.all(), write_only=True, required=False, allow_null=True
    )
    
    class Meta:
        model = Passenger
        fields = [
            'info', 'date_of_birth', 'nationality', 'passport_number',
            'passport_expiration_date', 'contact_number', 'notes', 'passport_document',
            'status'
        ]

# 3) Crew Lines
class CrewLineReadSerializer(serializers.ModelSerializer):
    primary_in_command = ContactSerializer(read_only=True)
    secondary_in_command = ContactSerializer(read_only=True)
    medics = ContactSerializer(source='medic_ids', many=True, read_only=True)
    
    class Meta:
        model = CrewLine
        fields = [
            'id', 'primary_in_command', 'secondary_in_command', 'medics',
            'status', 'created_on'
        ]

class CrewLineWriteSerializer(serializers.ModelSerializer):
    primary_in_command = serializers.PrimaryKeyRelatedField(
        queryset=Contact.objects.all(), write_only=True
    )
    secondary_in_command = serializers.PrimaryKeyRelatedField(
        queryset=Contact.objects.all(), write_only=True
    )
    medic_ids = serializers.PrimaryKeyRelatedField(
        source='medic_ids', queryset=Contact.objects.all(), many=True, write_only=True
    )
    
    class Meta:
        model = CrewLine
        fields = [
            'primary_in_command', 'secondary_in_command', 'medic_ids', 'status'
        ]

class TripMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = ("id", "trip_number", "type")


class TripLineReadSerializer(serializers.ModelSerializer):
    trip = TripMiniSerializer(source="trip_id", read_only=True)
    origin_airport = AirportSerializer(source="origin_airport_id", read_only=True)
    destination_airport = AirportSerializer(source="destination_airport_id", read_only=True)
    crew_line = CrewLineReadSerializer(source="crew_line_id", read_only=True)
    
    class Meta:
        model = TripLine
        fields = [
            'id', 'trip', 'origin_airport', 'destination_airport', 'crew_line',
            'departure_time_local', 'departure_time_utc', 'arrival_time_local',
            'arrival_time_utc', 'distance', 'flight_time', 'ground_time',
            'passenger_leg', 'status', 'created_on'
        ]
    
    def get_trip(self, obj):
        # Return minimal trip info to avoid circular references
        return {
            'id': obj.trip.id,
            'trip_number': obj.trip.trip_number,
            'type': obj.trip.type
        }

class TripLineWriteSerializer(serializers.ModelSerializer):
    trip = serializers.PrimaryKeyRelatedField(
        queryset=Trip.objects.all(), write_only=True
    )
    origin_airport = serializers.PrimaryKeyRelatedField(
        queryset=Airport.objects.all(), write_only=True
    )
    destination_airport = serializers.PrimaryKeyRelatedField(
        queryset=Airport.objects.all(), write_only=True
    )
    crew_line = serializers.PrimaryKeyRelatedField(
        queryset=CrewLine.objects.all(), write_only=True, required=False, allow_null=True
    )
    
    class Meta:
        model = TripLine
        fields = [
            'trip', 'origin_airport', 'destination_airport', 'crew_line',
            'departure_time_local', 'departure_time_utc', 'arrival_time_local',
            'arrival_time_utc', 'distance', 'flight_time', 'ground_time',
            'passenger_leg', 'status'
        ]

# 5) Trips
class TripReadSerializer(serializers.ModelSerializer):
    quote = serializers.SerializerMethodField()
    patient = serializers.SerializerMethodField()
    aircraft = AircraftSerializer(read_only=True)
    trip_lines = TripLineReadSerializer(many=True, read_only=True)
    passengers_data = PassengerReadSerializer(source='passengers', many=True, read_only=True)
    
    class Meta:
        model = Trip
        fields = [
            'id', 'email_chain', 'quote', 'type', 'patient', 'estimated_departure_time',
            'post_flight_duty_time', 'pre_flight_duty_time', 'aircraft', 'trip_number',
            'trip_lines', 'passengers_data', 'status', 'created_on'
        ]
    
    def get_quote(self, obj):
        if obj.quote:
            return {
                'id': obj.quote.id,
                'quoted_amount': obj.quote.quoted_amount,
                'status': obj.quote.status
            }
        return None
    
    def get_patient(self, obj):
        if obj.patient:
            return {
                'id': obj.patient.id,
                'status': obj.patient.status,
                'info': ContactSerializer(obj.patient.info).data
            }
        return None

class TripWriteSerializer(serializers.ModelSerializer):
    quote = serializers.PrimaryKeyRelatedField(
        queryset=Quote.objects.all(), write_only=True, required=False, allow_null=True
    )
    patient = serializers.PrimaryKeyRelatedField(
        queryset=Patient.objects.all(), write_only=True, required=False, allow_null=True
    )
    aircraft = serializers.PrimaryKeyRelatedField(
        queryset=Aircraft.objects.all(), write_only=True, required=False, allow_null=True
    )
    passenger_ids = serializers.PrimaryKeyRelatedField(
        source='passengers', queryset=Passenger.objects.all(), many=True, write_only=True, required=False
    )
    
    class Meta:
        model = Trip
        fields = [
            'email_chain', 'quote', 'type', 'patient', 'estimated_departure_time',
            'post_flight_duty_time', 'pre_flight_duty_time', 'aircraft', 'trip_number',
            'passenger_ids', 'status'
        ]

# 6) Quotes
class QuoteReadSerializer(serializers.ModelSerializer):
    contact = ContactSerializer(read_only=True)
    pickup_airport = AirportSerializer(read_only=True)
    dropoff_airport = AirportSerializer(read_only=True)
    patient = serializers.SerializerMethodField()
    payment_agreement = AgreementSerializer(read_only=True)
    consent_for_transport = AgreementSerializer(read_only=True)
    patient_service_agreement = AgreementSerializer(read_only=True)
    transactions = serializers.SerializerMethodField()
    
    class Meta:
        model = Quote
        fields = [
            'id', 'quoted_amount', 'contact', 'pickup_airport', 'dropoff_airport',
            'patient', 'payment_agreement', 'consent_for_transport', 'patient_service_agreement',
            'transactions', 'status', 'created_on'
        ]
    
    def get_patient(self, obj):
        if obj.patient:
            return {
                'id': obj.patient.id,
                'status': obj.patient.status
            }
        return None
    
    def get_transactions(self, obj):
        return [{
            'id': t.id,
            'amount': t.amount,
            'status': t.status
        } for t in obj.transactions.all()]

class QuoteWriteSerializer(serializers.ModelSerializer):
    contact = serializers.PrimaryKeyRelatedField(
        queryset=Contact.objects.all(), write_only=True
    )
    pickup_airport = serializers.PrimaryKeyRelatedField(
        queryset=Airport.objects.all(), write_only=True
    )
    dropoff_airport = serializers.PrimaryKeyRelatedField(
        queryset=Airport.objects.all(), write_only=True
    )
    patient = serializers.PrimaryKeyRelatedField(
        queryset=Patient.objects.all(), write_only=True, required=False, allow_null=True
    )
    payment_agreement = serializers.PrimaryKeyRelatedField(
        queryset=Agreement.objects.all(), write_only=True, required=False, allow_null=True
    )
    consent_for_transport = serializers.PrimaryKeyRelatedField(
        queryset=Agreement.objects.all(), write_only=True, required=False, allow_null=True
    )
    patient_service_agreement = serializers.PrimaryKeyRelatedField(
        queryset=Agreement.objects.all(), write_only=True, required=False, allow_null=True
    )
    transaction_ids = serializers.PrimaryKeyRelatedField(
        source='transactions', queryset=Transaction.objects.all(), many=True, write_only=True, required=False
    )
    
    class Meta:
        model = Quote
        fields = [
            'quoted_amount', 'contact', 'pickup_airport', 'dropoff_airport',
            'patient', 'payment_agreement', 'consent_for_transport',
            'patient_service_agreement', 'transaction_ids', 'status'
        ]

# 7) Documents
class DocumentReadSerializer(serializers.ModelSerializer):
    content_type = serializers.SerializerMethodField()
    download_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Document
        fields = ['id', 'filename', 'flag', 'content_type', 'download_url', 'created_on']
    
    def get_content_type(self, obj):
        # Return MIME type based on file extension
        import mimetypes
        return mimetypes.guess_type(obj.filename)[0] or 'application/octet-stream'
    
    def get_download_url(self, obj):
        # Return download URL for the document
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(f'/api/documents/{obj.id}/download/')
        return f'/api/documents/{obj.id}/download/'

class DocumentUploadSerializer(serializers.ModelSerializer):
    content = serializers.FileField(write_only=True)
    
    class Meta:
        model = Document
        fields = ['id', 'filename', 'content', 'flag']

# 8) Transactions
class TransactionPublicReadSerializer(serializers.ModelSerializer):
    """Minimal safe fields for public access by key"""
    class Meta:
        model = Transaction
        fields = ['id', 'amount', 'status', 'created_on']

class TransactionReadSerializer(serializers.ModelSerializer):
    """Full details for staff access"""
    class Meta:
        model = Transaction
        fields = '__all__'

class TransactionProcessWriteSerializer(serializers.ModelSerializer):
    """For processing payments with gateway inputs"""
    class Meta:
        model = Transaction
        fields = ['amount', 'status', 'payment_method', 'gateway_response']

# 9) Patient (updated to follow pattern)
class PatientReadSerializer(serializers.ModelSerializer):
    info = ContactSerializer(read_only=True)
    
    class Meta:
        model = Patient
        fields = ['id', 'info', 'status', 'created_on']

class PatientWriteSerializer(serializers.ModelSerializer):
    info = serializers.PrimaryKeyRelatedField(
        queryset=Contact.objects.all(), write_only=True
    )
    
    class Meta:
        model = Patient
        fields = ['info', 'status']
