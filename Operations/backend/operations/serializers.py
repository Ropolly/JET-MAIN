from rest_framework import serializers
from .models import Quote, Patient, Passenger, CrewLine, Trip, TripLine, TripEvent


class QuoteSerializer(serializers.ModelSerializer):
    """Serializer for Quote model with nested relationships."""
    
    contact_name = serializers.CharField(source='contact.business_name', read_only=True)
    pickup_airport_name = serializers.CharField(source='pickup_airport.name', read_only=True)
    dropoff_airport_name = serializers.CharField(source='dropoff_airport.name', read_only=True)
    patient_name = serializers.CharField(source='patient.info.first_name', read_only=True)
    
    class Meta:
        model = Quote
        fields = [
            'id', 'quoted_amount', 'contact', 'contact_name',
            'pickup_airport', 'pickup_airport_name',
            'dropoff_airport', 'dropoff_airport_name',
            'aircraft_type', 'estimated_flight_time', 'medical_team',
            'status', 'payment_status', 'inquiry_date',
            'patient', 'patient_name', 'includes_grounds',
            'number_of_stops', 'quote_pdf_status', 'quote_pdf_email',
            'cruise_doctor_first_name', 'cruise_doctor_last_name',
            'cruise_line', 'cruise_ship', 'created_on', 'modified_on'
        ]
        read_only_fields = ['id', 'created_on', 'modified_on']
    
    def validate_aircraft_type(self, value):
        """Validate aircraft type selection."""
        valid_types = ['65', '35', 'TBD']
        if value not in valid_types:
            raise serializers.ValidationError(f"Aircraft type must be one of: {valid_types}")
        return value
    
    def validate_medical_team(self, value):
        """Validate medical team configuration."""
        valid_teams = ['RN/RN', 'RN/Paramedic', 'RN/MD', 'RN/RT', 'standard', 'full']
        if value not in valid_teams:
            raise serializers.ValidationError(f"Medical team must be one of: {valid_teams}")
        return value


class PatientSerializer(serializers.ModelSerializer):
    """Serializer for Patient model with contact information."""
    
    contact_name = serializers.CharField(source='info.first_name', read_only=True)
    contact_email = serializers.EmailField(source='info.email', read_only=True)
    
    class Meta:
        model = Patient
        fields = [
            'id', 'info', 'contact_name', 'contact_email',
            'bed_at_origin', 'bed_at_destination', 'date_of_birth',
            'nationality', 'passport_number', 'passport_expiration_date',
            'special_instructions', 'status', 'passport_document',
            'letter_of_medical_necessity', 'created_on', 'modified_on'
        ]
        read_only_fields = ['id', 'created_on', 'modified_on']
    
    def validate_passport_expiration_date(self, value):
        """Validate passport is not expired."""
        from django.utils import timezone
        if value <= timezone.now().date():
            raise serializers.ValidationError("Passport expiration date must be in the future")
        return value


class PassengerSerializer(serializers.ModelSerializer):
    """Serializer for Passenger model."""
    
    contact_name = serializers.CharField(source='info.first_name', read_only=True)
    contact_email = serializers.EmailField(source='info.email', read_only=True)
    
    class Meta:
        model = Passenger
        fields = [
            'id', 'info', 'contact_name', 'contact_email',
            'date_of_birth', 'nationality', 'passport_number',
            'passport_expiration_date', 'contact_number', 'notes',
            'passport_document', 'created_on', 'modified_on'
        ]
        read_only_fields = ['id', 'created_on', 'modified_on']


class CrewLineSerializer(serializers.ModelSerializer):
    """Serializer for CrewLine model with crew member details."""
    
    primary_name = serializers.CharField(source='primary_in_command.first_name', read_only=True)
    secondary_name = serializers.CharField(source='secondary_in_command.first_name', read_only=True)
    medic_names = serializers.SerializerMethodField()
    
    class Meta:
        model = CrewLine
        fields = [
            'id', 'primary_in_command', 'primary_name',
            'secondary_in_command', 'secondary_name',
            'medic_ids', 'medic_names', 'created_on', 'modified_on'
        ]
        read_only_fields = ['id', 'created_on', 'modified_on']
    
    def get_medic_names(self, obj):
        """Get names of all medics assigned to this crew line."""
        return [f"{medic.first_name} {medic.last_name}" for medic in obj.medic_ids.all()]
    
    def validate(self, data):
        """Validate crew line data."""
        if data.get('primary_in_command') == data.get('secondary_in_command'):
            raise serializers.ValidationError(
                "Primary and secondary pilots must be different people"
            )
        return data


class TripLineSerializer(serializers.ModelSerializer):
    """Serializer for TripLine model with airport and crew details."""
    
    origin_airport_name = serializers.CharField(source='origin_airport.name', read_only=True)
    destination_airport_name = serializers.CharField(source='destination_airport.name', read_only=True)
    departure_fbo_name = serializers.CharField(source='departure_fbo.name', read_only=True)
    arrival_fbo_name = serializers.CharField(source='arrival_fbo.name', read_only=True)
    
    class Meta:
        model = TripLine
        fields = [
            'id', 'trip', 'origin_airport', 'origin_airport_name',
            'destination_airport', 'destination_airport_name',
            'departure_fbo', 'departure_fbo_name',
            'arrival_fbo', 'arrival_fbo_name',
            'crew_line', 'departure_time_local', 'departure_time_utc',
            'arrival_time_local', 'arrival_time_utc',
            'distance', 'flight_time', 'ground_time', 'passenger_leg',
            'created_on', 'modified_on'
        ]
        read_only_fields = ['id', 'created_on', 'modified_on']
    
    def validate(self, data):
        """Validate trip line timing."""
        departure_utc = data.get('departure_time_utc')
        arrival_utc = data.get('arrival_time_utc')
        
        if departure_utc and arrival_utc and departure_utc >= arrival_utc:
            raise serializers.ValidationError(
                "Departure time must be before arrival time"
            )
        
        return data


class TripEventSerializer(serializers.ModelSerializer):
    """Serializer for TripEvent model."""
    
    airport_name = serializers.CharField(source='airport.name', read_only=True)
    
    class Meta:
        model = TripEvent
        fields = [
            'id', 'trip', 'airport', 'airport_name', 'event_type',
            'start_time_local', 'start_time_utc',
            'end_time_local', 'end_time_utc',
            'crew_line', 'notes', 'created_on', 'modified_on'
        ]
        read_only_fields = ['id', 'created_on', 'modified_on']
    
    def validate(self, data):
        """Validate trip event data."""
        event_type = data.get('event_type')
        end_time_utc = data.get('end_time_utc')
        
        # OVERNIGHT events must have end time
        if event_type == 'OVERNIGHT' and not end_time_utc:
            raise serializers.ValidationError(
                "Overnight events must have an end time"
            )
        
        # CREW_CHANGE events must have crew_line
        if event_type == 'CREW_CHANGE' and not data.get('crew_line'):
            raise serializers.ValidationError(
                "Crew change events must specify the new crew line"
            )
        
        return data


class TripSerializer(serializers.ModelSerializer):
    """Serializer for Trip model with nested relationships."""
    
    trip_lines = TripLineSerializer(many=True, read_only=True)
    events = TripEventSerializer(many=True, read_only=True)
    aircraft_tail_number = serializers.CharField(source='aircraft.tail_number', read_only=True)
    quote_amount = serializers.DecimalField(source='quote.quoted_amount', max_digits=10, decimal_places=2, read_only=True)
    patient_name = serializers.CharField(source='patient.info.first_name', read_only=True)
    
    class Meta:
        model = Trip
        fields = [
            'id', 'trip_number', 'type', 'quote', 'quote_amount',
            'patient', 'patient_name', 'aircraft', 'aircraft_tail_number',
            'estimated_departure_time', 'pre_flight_duty_time',
            'post_flight_duty_time', 'internal_itinerary',
            'customer_itinerary', 'passengers', 'notes',
            'email_chain', 'status', 'trip_lines', 'events',
            'created_on', 'modified_on'
        ]
        read_only_fields = ['id', 'created_on', 'modified_on']
    
    def validate_trip_number(self, value):
        """Validate trip number uniqueness."""
        if self.instance and self.instance.trip_number == value:
            return value  # No change, skip validation
        
        if Trip.objects.filter(trip_number=value).exists():
            raise serializers.ValidationError("Trip number must be unique")
        
        return value
    
    def validate(self, data):
        """Validate trip data based on type."""
        trip_type = data.get('type')
        patient = data.get('patient')
        
        # Medical trips must have a patient
        if trip_type == 'medical' and not patient:
            raise serializers.ValidationError(
                "Medical trips must have an associated patient"
            )
        
        return data


class TripTimelineSerializer(serializers.Serializer):
    """Serializer for trip timeline view."""
    
    type = serializers.CharField()
    time_utc = serializers.DateTimeField()
    time_local = serializers.DateTimeField()
    event = serializers.CharField()
    location = serializers.CharField()
    details = serializers.JSONField()
