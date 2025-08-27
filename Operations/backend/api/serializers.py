from rest_framework import serializers
from .models import (
    Modification, Permission, Role, Department, UserProfile, Contact, 
    FBO, Ground, Airport, Document, Aircraft, Transaction, Agreement,
    Patient, Quote, Passenger, CrewLine, Trip, TripLine, Staff, StaffRole,
    StaffRoleMembership, TripEvent
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
    contact_type = serializers.SerializerMethodField()
    
    class Meta:
        model = Contact
        fields = ['id', 'first_name', 'last_name', 'business_name', 'email', 'phone', 
                 'address_line1', 'address_line2', 'city', 'state', 'zip', 'country',
                 'nationality', 'date_of_birth', 'passport_number', 'passport_expiration_date',
                 'contact_type', 'created_on', 'created_by', 'modified_on', 'modified_by']
    
    def get_contact_type(self, obj):
        """
        Determine contact type based on related objects
        """
        # Check if this contact is a patient
        if hasattr(obj, 'patients') and obj.patients.exists():
            return 'Patient'
        
        # Check if this contact is staff
        if hasattr(obj, 'staff'):
            try:
                staff = obj.staff
                # Check staff role memberships to determine if pilot or medic
                role_codes = staff.role_memberships.filter(
                    end_on__isnull=True  # Active memberships only
                ).values_list('role__code', flat=True)
                
                if 'PIC' in role_codes or 'SIC' in role_codes:
                    return 'Staff - Pilot'
                elif 'RN' in role_codes or 'PARAMEDIC' in role_codes:
                    return 'Staff - Medic'
                else:
                    return 'Staff'
            except:
                return 'Staff'
        
        # Check if this contact is a passenger
        if hasattr(obj, 'passengers') and obj.passengers.exists():
            return 'Passenger'
        
        # Check if this contact is a customer (has quotes)
        if hasattr(obj, 'quotes') and obj.quotes.exists():
            return 'Customer'
        
        # Default type
        return 'General'

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
    fbos = FBOSerializer(many=True, read_only=True)
    grounds = GroundSerializer(many=True, read_only=True)
    fbos_count = serializers.SerializerMethodField()
    grounds_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Airport
        fields = ['id', 'ident', 'name', 'latitude', 'longitude', 'elevation', 
                 'iso_country', 'iso_region', 'municipality', 'icao_code', 'iata_code', 
                 'local_code', 'gps_code', 'airport_type', 'timezone', 
                 'fbos', 'grounds', 'fbos_count', 'grounds_count',
                 'created_on', 'created_by', 'modified_on', 'modified_by']
    
    def get_fbos_count(self, obj):
        return obj.fbos.count()
    
    def get_grounds_count(self, obj):
        return obj.grounds.count()

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
    related_passengers = serializers.SerializerMethodField()
    
    class Meta:
        model = Passenger
        fields = [
            'id', 'info', 'date_of_birth', 'nationality', 'passport_number',
            'passport_expiration_date', 'contact_number', 'notes', 'passport_document',
            'related_passengers', 'status', 'created_on'
        ]
    
    def get_related_passengers(self, obj):
        return [{'id': p.id, 'info': ContactSerializer(p.info).data} for p in obj.passenger_ids.all()]

class PassengerWriteSerializer(serializers.ModelSerializer):
    info = serializers.PrimaryKeyRelatedField(
        queryset=Contact.objects.all(), write_only=True
    )
    passport_document = serializers.PrimaryKeyRelatedField(
        queryset=Document.objects.all(), write_only=True, required=False, allow_null=True
    )
    passenger_ids = serializers.PrimaryKeyRelatedField(
        queryset=Passenger.objects.all(), many=True, write_only=True, required=False
    )
    
    class Meta:
        model = Passenger
        fields = [
            'info', 'date_of_birth', 'nationality', 'passport_number',
            'passport_expiration_date', 'contact_number', 'notes', 'passport_document',
            'passenger_ids', 'status'
        ]
    
    def create(self, validated_data):
        # Get contact data for filling deprecated fields
        contact = validated_data['info']
        passenger_ids = validated_data.pop('passenger_ids', [])
        
        # Use contact data as primary source, fallback to provided data
        validated_data['date_of_birth'] = contact.date_of_birth or validated_data.get('date_of_birth')
        validated_data['nationality'] = contact.nationality or validated_data.get('nationality', '')
        validated_data['passport_number'] = contact.passport_number or validated_data.get('passport_number', '')
        validated_data['passport_expiration_date'] = contact.passport_expiration_date or validated_data.get('passport_expiration_date')
        
        passenger = super().create(validated_data)
        
        # Set related passengers if provided
        if passenger_ids:
            passenger.passenger_ids.set(passenger_ids)
        
        return passenger

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
        queryset=Contact.objects.all(), many=True, write_only=True
    )
    
    class Meta:
        model = CrewLine
        fields = [
            'id', 'primary_in_command', 'secondary_in_command', 'medic_ids', 'status'
        ]

class TripMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = ("id", "trip_number", "type")


class TripLineReadSerializer(serializers.ModelSerializer):
    trip = TripMiniSerializer(read_only=True)
    origin_airport = AirportSerializer(read_only=True)
    destination_airport = AirportSerializer(read_only=True)
    crew_line = CrewLineReadSerializer(read_only=True)
    departure_fbo = FBOSerializer(read_only=True)
    arrival_fbo = FBOSerializer(read_only=True)
    
    class Meta:
        model = TripLine
        fields = [
            'id', 'trip', 'origin_airport', 'destination_airport', 'crew_line',
            'departure_fbo', 'arrival_fbo', 'departure_time_local', 'departure_time_utc', 
            'arrival_time_local', 'arrival_time_utc', 'distance', 'flight_time', 
            'ground_time', 'passenger_leg', 'status', 'created_on'
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
    departure_fbo = serializers.PrimaryKeyRelatedField(
        queryset=FBO.objects.all(), write_only=True, required=False, allow_null=True
    )
    arrival_fbo = serializers.PrimaryKeyRelatedField(
        queryset=FBO.objects.all(), write_only=True, required=False, allow_null=True
    )
    
    class Meta:
        model = TripLine
        fields = [
            'id', 'trip', 'origin_airport', 'destination_airport', 'crew_line',
            'departure_fbo', 'arrival_fbo', 'departure_time_local', 'departure_time_utc', 
            'arrival_time_local', 'arrival_time_utc', 'distance', 'flight_time', 
            'ground_time', 'passenger_leg', 'status'
        ]

# 4.5) Trip Events
class TripEventWriteSerializer(serializers.ModelSerializer):
    trip_id = serializers.PrimaryKeyRelatedField(source='trip', queryset=Trip.objects.all())
    airport_id = serializers.PrimaryKeyRelatedField(source='airport', queryset=Airport.objects.all())
    crew_line_id = serializers.PrimaryKeyRelatedField(
        source='crew_line', queryset=CrewLine.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = TripEvent
        fields = (
            "id",
            "trip_id",
            "airport_id",
            "event_type",
            "start_time_local",
            "start_time_utc",
            "end_time_local",
            "end_time_utc",
            "crew_line_id",
            "notes",
        )

    def validate(self, attrs):
        ev_type = attrs.get("event_type") or (self.instance and self.instance.event_type)
        if ev_type == "CREW_CHANGE":
            # Check for 'crew_line' in attrs because the field uses source='crew_line'
            if not attrs.get("crew_line") and not (self.instance and self.instance.crew_line):
                raise serializers.ValidationError({"crew_line_id": "Required for CREW_CHANGE"})
            # end_time is not required for crew change; treat as instantaneous or short window

        if ev_type == "OVERNIGHT":
            st = attrs.get("start_time_utc") or (self.instance and self.instance.start_time_utc)
            et = attrs.get("end_time_utc") or (self.instance and self.instance.end_time_utc)
            if not (st and et):
                raise serializers.ValidationError({"end_time_utc": "OVERNIGHT requires start and end times"})
            if et <= st:
                raise serializers.ValidationError({"end_time_utc": "Must be after start_time_utc"})
        return attrs


class TripEventReadSerializer(serializers.ModelSerializer):
    # Return IDs to match your API style
    trip_id = serializers.PrimaryKeyRelatedField(source='trip', read_only=True)
    airport_id = serializers.PrimaryKeyRelatedField(source='airport', read_only=True)
    crew_line_id = serializers.PrimaryKeyRelatedField(source='crew_line', read_only=True)

    class Meta:
        model = TripEvent
        fields = (
            "id",
            "trip_id",
            "airport_id",
            "event_type",
            "start_time_local",
            "start_time_utc",
            "end_time_local",
            "end_time_utc",
            "crew_line_id",
            "notes",
            "created_on",
        )

# 5) Trips
class TripReadSerializer(serializers.ModelSerializer):
    quote = serializers.SerializerMethodField()
    patient = serializers.SerializerMethodField()
    aircraft = AircraftSerializer(read_only=True)
    trip_lines = TripLineReadSerializer(many=True, read_only=True)
    passengers_data = PassengerReadSerializer(source='passengers', many=True, read_only=True)
    events = TripEventReadSerializer(many=True, read_only=True)
    
    class Meta:
        model = Trip
        fields = [
            'id', 'email_chain', 'quote', 'type', 'patient', 'estimated_departure_time',
            'post_flight_duty_time', 'pre_flight_duty_time', 'aircraft', 'trip_number',
            'trip_lines', 'passengers_data', 'events', 'status', 'created_on'
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
            'id', 'email_chain', 'quote', 'type', 'patient', 'estimated_departure_time',
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
            'transactions', 'status', 'quote_pdf_status', 'aircraft_type', 'medical_team',
            'created_on'
        ]
    
    def get_patient(self, obj):
        if obj.patient:
            patient_data = {
                'id': obj.patient.id,
                'status': obj.patient.status
            }
            # Include patient's contact info (name)
            if obj.patient.info:
                patient_data['info'] = {
                    'id': obj.patient.info.id,
                    'first_name': obj.patient.info.first_name,
                    'last_name': obj.patient.info.last_name,
                    'email': obj.patient.info.email
                }
            return patient_data
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
            'patient', 'aircraft_type', 'medical_team', 'estimated_flight_time',
            'number_of_stops', 'includes_grounds', 'cruise_line', 'cruise_ship',
            'cruise_doctor_first_name', 'cruise_doctor_last_name', 'quote_pdf_email',
            'payment_agreement', 'consent_for_transport', 'patient_service_agreement', 
            'transaction_ids', 'status'
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
        fields = [
            'id', 
            'info', 
            'date_of_birth', 
            'nationality', 
            'passport_number', 
            'passport_expiration_date', 
            'special_instructions', 
            'status', 
            'bed_at_origin', 
            'bed_at_destination', 
            'created_on'
        ]

class PatientWriteSerializer(serializers.ModelSerializer):
    info = serializers.PrimaryKeyRelatedField(
        queryset=Contact.objects.all(), write_only=True
    )
    
    class Meta:
        model = Patient
        fields = [
            'info', 
            'date_of_birth', 
            'nationality', 
            'passport_number', 
            'passport_expiration_date', 
            'special_instructions', 
            'status', 
            'bed_at_origin', 
            'bed_at_destination'
        ]
    
    def create(self, validated_data):
        # Get contact data for filling deprecated fields
        contact = validated_data['info']
        
        # Use contact data as primary source, fallback to provided data
        validated_data['date_of_birth'] = contact.date_of_birth or validated_data.get('date_of_birth')
        validated_data['nationality'] = contact.nationality or validated_data.get('nationality', '')
        validated_data['passport_number'] = contact.passport_number or validated_data.get('passport_number', '')
        validated_data['passport_expiration_date'] = contact.passport_expiration_date or validated_data.get('passport_expiration_date')
        
        return super().create(validated_data)


class StaffWriteSerializer(serializers.ModelSerializer):
    # Accept a Contact id on write
    contact_id = serializers.PrimaryKeyRelatedField(
        source="contact", queryset=Contact.objects.all()
    )

    class Meta:
        model = Staff
        fields = ("id", "contact_id", "active", "notes")

    def validate_contact_id(self, contact: Contact):
        # Friendly error if a Staff already exists for the Contact (OneToOne is also enforced by DB)
        if self.instance is None and Staff.objects.filter(contact=contact).exists():
            raise serializers.ValidationError("Staff for this contact already exists.")
        return contact


# --- StaffRole ---

class StaffRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffRole
        fields = ("id", "code", "name", "created_on")


# --- StaffRoleMembership ---

class StaffRoleMembershipWriteSerializer(serializers.ModelSerializer):
    staff_id = serializers.PrimaryKeyRelatedField(
        source="staff", queryset=Staff.objects.all()
    )
    role_id = serializers.PrimaryKeyRelatedField(
        source="role", queryset=StaffRole.objects.all()
    )

    class Meta:
        model = StaffRoleMembership
        fields = ("id", "staff_id", "role_id", "start_on", "end_on")

    def validate(self, attrs):
        start_on = attrs.get("start_on")
        end_on = attrs.get("end_on")
        if start_on and end_on and end_on < start_on:
            raise serializers.ValidationError({"end_on": "end_on cannot be before start_on"})
        return attrs


class StaffRoleMembershipReadSerializer(serializers.ModelSerializer):
    staff_id = serializers.PrimaryKeyRelatedField(source="staff", read_only=True)
    role_id = serializers.PrimaryKeyRelatedField(source="role", read_only=True)
    role = StaffRoleSerializer(read_only=True)

    class Meta:
        model = StaffRoleMembership
        fields = ("id", "staff_id", "role_id", "role", "start_on", "end_on", "created_on")


class StaffReadSerializer(serializers.ModelSerializer):
    # Return the FK as an id to stay consistent with your API style
    contact_id = serializers.PrimaryKeyRelatedField(source="contact", read_only=True)
    # Include full contact information for display purposes
    contact = ContactSerializer(read_only=True)
    # Include role memberships for display purposes
    role_memberships = StaffRoleMembershipReadSerializer(many=True, read_only=True)

    class Meta:
        model = Staff
        fields = ("id", "contact_id", "contact", "active", "notes", "created_on", "role_memberships")
