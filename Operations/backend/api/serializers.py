from rest_framework import serializers
from .models import (
    Modification, Permission, Role, Department, UserProfile, Contact, 
    FBO, Ground, Airport, Document, Aircraft, Transaction, Agreement,
    Patient, Quote, Passenger, CrewLine, Trip, TripLine, Staff, StaffRole,
    StaffRoleMembership, TripEvent, Comment
)
from django.contrib.auth.models import User

# User serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff']

# Base serializers
class ModificationSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Modification
        fields = ['id', 'model', 'content_type', 'object_id', 'field', 'before', 'after', 'time', 'user', 'user_username']

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

class CommentSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    created_by_name = serializers.SerializerMethodField(read_only=True)
    content_type_name = serializers.CharField(source='content_type.model', read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'content_type', 'content_type_name', 'object_id', 'text', 
                 'created_on', 'created_by', 'created_by_username', 'created_by_name',
                 'modified_on', 'modified_by', 'status']
    
    def get_created_by_name(self, obj):
        if obj.created_by:
            if hasattr(obj.created_by, 'profile'):
                return f"{obj.created_by.profile.first_name} {obj.created_by.profile.last_name}".strip()
            return obj.created_by.username
        return None

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
    airport_codes = serializers.SerializerMethodField()
    airport_names = serializers.SerializerMethodField()
    contacts = serializers.PrimaryKeyRelatedField(many=True, queryset=Contact.objects.all(), required=False)
    
    class Meta:
        model = FBO
        fields = ['id', 'name', 'address_line1', 'address_line2', 'city', 'state', 'zip', 
                 'country', 'phone', 'phone_secondary', 'email', 'notes', 'contacts',
                 'airport_codes', 'airport_names', 'created_on', 'created_by', 'modified_on', 'modified_by']
    
    def get_airport_codes(self, obj):
        airports = obj.airports.all()
        return [airport.ident for airport in airports] if airports else []
    
    def get_airport_names(self, obj):
        airports = obj.airports.all()
        return [airport.name for airport in airports] if airports else []

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
    trips = serializers.SerializerMethodField()
    
    class Meta:
        model = Passenger
        fields = [
            'id', 'info', 'date_of_birth', 'nationality', 'passport_number',
            'passport_expiration_date', 'contact_number', 'notes', 'passport_document',
            'related_passengers', 'trips', 'status', 'created_on'
        ]
    
    def get_related_passengers(self, obj):
        return [{'id': p.id, 'info': ContactSerializer(p.info).data} for p in obj.passenger_ids.all()]
    
    def get_trips(self, obj):
        trips = obj.trips.all()
        return [{'id': trip.id, 'trip_number': trip.trip_number} for trip in trips]

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
    departure_timezone_info = serializers.SerializerMethodField()
    arrival_timezone_info = serializers.SerializerMethodField()
    
    class Meta:
        model = TripLine
        fields = [
            'id', 'trip', 'origin_airport', 'destination_airport', 'crew_line',
            'departure_fbo', 'arrival_fbo', 'departure_time_local', 'departure_time_utc', 
            'arrival_time_local', 'arrival_time_utc', 'distance', 'flight_time', 
            'ground_time', 'passenger_leg', 'status', 'created_on',
            'departure_timezone_info', 'arrival_timezone_info'
        ]
    
    def get_departure_timezone_info(self, obj):
        """Get timezone information for departure airport."""
        print(f"DEBUG: get_departure_timezone_info called for trip line {obj.id}")
        print(f"DEBUG: origin_airport exists: {bool(obj.origin_airport)}")
        if obj.origin_airport:
            print(f"DEBUG: origin_airport timezone: {getattr(obj.origin_airport, 'timezone', 'NO_TIMEZONE_FIELD')}")
        
        if not obj.origin_airport or not obj.origin_airport.timezone:
            print(f"DEBUG: Returning None - no airport or no timezone")
            return None
        
        try:
            from .timezone_utils import get_timezone_info, format_time_with_timezone, convert_utc_to_local
            
            # Use UTC time as source of truth and calculate local time
            if not obj.departure_time_utc:
                print("DEBUG: No departure UTC time available")
                return None
                
            print(f"DEBUG: Converting UTC {obj.departure_time_utc} to {obj.origin_airport.timezone}")
            
            # Convert UTC to proper local time for this airport
            local_time = convert_utc_to_local(obj.departure_time_utc, obj.origin_airport.timezone)
            print(f"DEBUG: Calculated local time: {local_time}")
            
            # Get timezone info for this time
            tz_info = get_timezone_info(obj.origin_airport.timezone, obj.departure_time_utc)
            print(f"DEBUG: Timezone info: {tz_info}")
            
            # Format the calculated local time with timezone info
            formatted_time = format_time_with_timezone(
                local_time, obj.origin_airport.timezone, include_utc=True
            )
            print(f"DEBUG: Formatted time: {formatted_time}")
            tz_info['formatted_time'] = formatted_time
            
            # Also add the calculated local time for reference
            tz_info['calculated_local_time'] = local_time.isoformat()
            
            print(f"DEBUG: Final timezone info: {tz_info}")
            return tz_info
        except Exception as e:
            # Log the error for debugging
            print(f"DEBUG: Exception in get_departure_timezone_info: {str(e)}")
            import traceback
            print(f"DEBUG: Traceback: {traceback.format_exc()}")
            return None
    
    def get_arrival_timezone_info(self, obj):
        """Get timezone information for arrival airport."""
        print(f"DEBUG: get_arrival_timezone_info called for trip line {obj.id}")
        print(f"DEBUG: destination_airport exists: {bool(obj.destination_airport)}")
        if obj.destination_airport:
            print(f"DEBUG: destination_airport timezone: {getattr(obj.destination_airport, 'timezone', 'NO_TIMEZONE_FIELD')}")
        
        if not obj.destination_airport or not obj.destination_airport.timezone:
            print(f"DEBUG: Returning None - no airport or no timezone")
            return None
        
        try:
            from .timezone_utils import get_timezone_info, format_time_with_timezone, convert_utc_to_local
            
            # Use UTC time as source of truth and calculate local time
            if not obj.arrival_time_utc:
                print("DEBUG: No arrival UTC time available")
                return None
                
            print(f"DEBUG: Converting UTC {obj.arrival_time_utc} to {obj.destination_airport.timezone}")
            
            # Convert UTC to proper local time for this airport
            local_time = convert_utc_to_local(obj.arrival_time_utc, obj.destination_airport.timezone)
            print(f"DEBUG: Calculated arrival local time: {local_time}")
            
            # Get timezone info for this time
            tz_info = get_timezone_info(obj.destination_airport.timezone, obj.arrival_time_utc)
            print(f"DEBUG: Arrival timezone info: {tz_info}")
            
            # Format the calculated local time with timezone info
            formatted_time = format_time_with_timezone(
                local_time, obj.destination_airport.timezone, include_utc=True
            )
            print(f"DEBUG: Arrival formatted time: {formatted_time}")
            tz_info['formatted_time'] = formatted_time
            
            # Also add the calculated local time for reference
            tz_info['calculated_local_time'] = local_time.isoformat()
            
            print(f"DEBUG: Final arrival timezone info: {tz_info}")
            return tz_info
        except Exception:
            return None
    
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
    
    # Make time fields optional for auto-calculation
    departure_time_utc = serializers.DateTimeField(required=False, allow_null=True)
    arrival_time_local = serializers.DateTimeField(required=False, allow_null=True)
    arrival_time_utc = serializers.DateTimeField(required=False, allow_null=True)
    
    class Meta:
        model = TripLine
        fields = [
            'id', 'trip', 'origin_airport', 'destination_airport', 'crew_line',
            'departure_fbo', 'arrival_fbo', 'departure_time_local', 'departure_time_utc', 
            'arrival_time_local', 'arrival_time_utc', 'distance', 'flight_time', 
            'ground_time', 'passenger_leg', 'status'
        ]
    
    def validate(self, data):
        """
        Validate timezone consistency and auto-calculate missing times.
        """
        from .timezone_utils import (
            convert_local_to_utc, convert_utc_to_local, 
            validate_time_consistency, check_dst_transition_warning
        )
        
        origin_airport = data.get('origin_airport')
        destination_airport = data.get('destination_airport')
        
        # Get timezone info
        origin_timezone = origin_airport.timezone if origin_airport else None
        destination_timezone = destination_airport.timezone if destination_airport else None
        
        departure_local = data.get('departure_time_local')
        departure_utc = data.get('departure_time_utc')
        arrival_local = data.get('arrival_time_local')
        arrival_utc = data.get('arrival_time_utc')
        
        print(f"DEBUG: Received data - departure_local: {departure_local}, departure_utc: {departure_utc}")
        print(f"DEBUG: Received data - arrival_local: {arrival_local}, arrival_utc: {arrival_utc}")
        print(f"DEBUG: Flight time: {data.get('flight_time')}")
        print(f"DEBUG: Origin timezone: {origin_timezone}, Destination timezone: {destination_timezone}")
        
        # Convert timezone-aware datetimes to naive for our timezone functions
        if departure_local and hasattr(departure_local, 'tzinfo') and departure_local.tzinfo:
            departure_local = departure_local.replace(tzinfo=None)
        if arrival_local and hasattr(arrival_local, 'tzinfo') and arrival_local.tzinfo:
            arrival_local = arrival_local.replace(tzinfo=None)
        
        # Validate and auto-calculate departure times
        if departure_local and origin_timezone:
            # Check for DST issues
            dst_warning = check_dst_transition_warning(departure_local, origin_timezone)
            if dst_warning and dst_warning['type'] == 'non_existent':
                raise serializers.ValidationError(
                    f"Departure time issue: {dst_warning['message']} {dst_warning['suggestion']}"
                )
            
            # Auto-calculate UTC from local if missing or inconsistent
            if not departure_utc:
                data['departure_time_utc'] = convert_local_to_utc(departure_local, origin_timezone)
            elif not validate_time_consistency(departure_local, departure_utc, origin_timezone):
                # Local time takes precedence, recalculate UTC
                data['departure_time_utc'] = convert_local_to_utc(departure_local, origin_timezone)
                
        elif departure_utc and origin_timezone:
            # Calculate local from UTC if local is missing
            if not departure_local:
                data['departure_time_local'] = convert_utc_to_local(departure_utc, origin_timezone)
        
        # Validate and auto-calculate arrival times
        if arrival_local and destination_timezone:
            # Check for DST issues
            dst_warning = check_dst_transition_warning(arrival_local, destination_timezone)
            if dst_warning and dst_warning['type'] == 'non_existent':
                raise serializers.ValidationError(
                    f"Arrival time issue: {dst_warning['message']} {dst_warning['suggestion']}"
                )
            
            # Auto-calculate UTC from local if missing or inconsistent
            if not arrival_utc:
                data['arrival_time_utc'] = convert_local_to_utc(arrival_local, destination_timezone)
            elif not validate_time_consistency(arrival_local, arrival_utc, destination_timezone):
                # Local time takes precedence, recalculate UTC
                data['arrival_time_utc'] = convert_local_to_utc(arrival_local, destination_timezone)
                
        elif arrival_utc and destination_timezone:
            # Calculate local from UTC if local is missing
            if not arrival_local:
                data['arrival_time_local'] = convert_utc_to_local(arrival_utc, destination_timezone)
        
        # If arrival times are missing or None but we have departure time and flight time, calculate them PROPERLY
        print(f"DEBUG: Checking if should calculate arrivals - arrival_local: {arrival_local}, arrival_utc: {arrival_utc}")
        if (not arrival_local or arrival_local is None) and (not arrival_utc or arrival_utc is None):
            print("DEBUG: Arrival times are missing, attempting to calculate")
            departure_utc_time = data.get('departure_time_utc') or departure_utc
            flight_time = data.get('flight_time')
            
            print(f"DEBUG: For calculation - departure_utc_time: {departure_utc_time}, flight_time: {flight_time}, destination_timezone: {destination_timezone}")
            if departure_utc_time and flight_time and destination_timezone:
                try:
                    print(f"DEBUG: Calculating arrival from departure UTC: {departure_utc_time}, flight time: {flight_time}")
                    
                    # Parse flight_time - handle both string and timedelta formats
                    if isinstance(flight_time, str):
                        time_parts = flight_time.split(':')
                        flight_hours = int(time_parts[0]) + int(time_parts[1]) / 60.0
                        if len(time_parts) > 2:
                            flight_hours += int(time_parts[2]) / 3600.0
                    elif hasattr(flight_time, 'total_seconds'):  # timedelta object
                        flight_hours = flight_time.total_seconds() / 3600.0
                    else:
                        flight_hours = float(flight_time)
                    
                    print(f"DEBUG: Flight duration in hours: {flight_hours}")
                    
                    from datetime import datetime, timedelta
                    
                    # Ensure departure_utc_time is a datetime object
                    if isinstance(departure_utc_time, str):
                        departure_dt = datetime.fromisoformat(departure_utc_time.replace('Z', '+00:00'))
                        if departure_dt.tzinfo:
                            departure_dt = departure_dt.replace(tzinfo=None)
                    else:
                        departure_dt = departure_utc_time.replace(tzinfo=None) if departure_utc_time.tzinfo else departure_utc_time
                    
                    # Calculate arrival in UTC (proper flight time calculation)
                    arrival_utc_dt = departure_dt + timedelta(hours=flight_hours)
                    print(f"DEBUG: Calculated arrival UTC: {arrival_utc_dt}")
                    
                    # Set the UTC arrival time
                    data['arrival_time_utc'] = arrival_utc_dt
                    
                    # Convert UTC to local time for destination airport
                    arrival_local_dt = convert_utc_to_local(arrival_utc_dt, destination_timezone)
                    data['arrival_time_local'] = arrival_local_dt
                    print(f"DEBUG: Calculated arrival local ({destination_timezone}): {arrival_local_dt}")
                        
                except (ValueError, TypeError) as e:
                    print(f"DEBUG: Error calculating arrival times: {str(e)}")
                    # If calculation fails, let the user provide arrival times manually
                    pass
        
        return data

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
        """Validate trip event data and auto-calculate missing timezone conversions."""
        from .timezone_utils import (
            convert_local_to_utc, convert_utc_to_local, 
            validate_time_consistency, check_dst_transition_warning
        )
        
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

        # Timezone validation and auto-calculation
        airport = attrs.get("airport") or (self.instance and self.instance.airport)
        if airport and airport.timezone:
            warnings = []
            
            # Handle start time timezone conversion
            start_local = attrs.get("start_time_local")
            start_utc = attrs.get("start_time_utc")
            
            # Convert timezone-aware datetimes to naive for our timezone functions
            if start_local and hasattr(start_local, 'tzinfo') and start_local.tzinfo:
                start_local = start_local.replace(tzinfo=None)
            
            if start_local and start_utc:
                # Both provided - validate consistency
                if not validate_time_consistency(start_local, start_utc, airport.timezone):
                    warnings.append("start_time_local and start_time_utc are inconsistent with airport timezone")
            elif start_local and not start_utc:
                # Auto-calculate UTC from local
                try:
                    attrs['start_time_utc'] = convert_local_to_utc(start_local, airport.timezone)
                    # Check for DST warnings
                    dst_warning = check_dst_transition_warning(start_local, airport.timezone)
                    if dst_warning:
                        warnings.append(f"Start time: {dst_warning['message']}")
                except Exception as e:
                    raise serializers.ValidationError({"start_time_local": f"Invalid time for airport timezone: {str(e)}"})
            elif start_utc and not start_local:
                # Auto-calculate local from UTC
                try:
                    attrs['start_time_local'] = convert_utc_to_local(start_utc, airport.timezone)
                except Exception as e:
                    raise serializers.ValidationError({"start_time_utc": f"Cannot convert to airport timezone: {str(e)}"})

            # Handle end time timezone conversion (for OVERNIGHT events)
            end_local = attrs.get("end_time_local")
            end_utc = attrs.get("end_time_utc")
            
            # Convert timezone-aware datetimes to naive for our timezone functions
            if end_local and hasattr(end_local, 'tzinfo') and end_local.tzinfo:
                end_local = end_local.replace(tzinfo=None)
            
            if end_local and end_utc:
                # Both provided - validate consistency
                if not validate_time_consistency(end_local, end_utc, airport.timezone):
                    warnings.append("end_time_local and end_time_utc are inconsistent with airport timezone")
            elif end_local and not end_utc:
                # Auto-calculate UTC from local
                try:
                    attrs['end_time_utc'] = convert_local_to_utc(end_local, airport.timezone)
                    # Check for DST warnings
                    dst_warning = check_dst_transition_warning(end_local, airport.timezone)
                    if dst_warning:
                        warnings.append(f"End time: {dst_warning['message']}")
                except Exception as e:
                    raise serializers.ValidationError({"end_time_local": f"Invalid time for airport timezone: {str(e)}"})
            elif end_utc and not end_local:
                # Auto-calculate local from UTC
                try:
                    attrs['end_time_local'] = convert_utc_to_local(end_utc, airport.timezone)
                except Exception as e:
                    raise serializers.ValidationError({"end_time_utc": f"Cannot convert to airport timezone: {str(e)}"})

            # Store warnings for potential frontend display
            if warnings:
                if not hasattr(self, '_timezone_warnings'):
                    self._timezone_warnings = []
                self._timezone_warnings.extend(warnings)

        return attrs


class TripEventReadSerializer(serializers.ModelSerializer):
    # Return IDs to match your API style
    trip_id = serializers.PrimaryKeyRelatedField(source='trip', read_only=True)
    airport_id = serializers.PrimaryKeyRelatedField(source='airport', read_only=True)
    crew_line_id = serializers.PrimaryKeyRelatedField(source='crew_line', read_only=True)
    airport_timezone_info = serializers.SerializerMethodField()

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
            "airport_timezone_info",
        )
    
    def get_airport_timezone_info(self, obj):
        """Get timezone information for the event's airport."""
        if not obj.airport or not obj.airport.timezone:
            return None
        
        try:
            from .timezone_utils import get_timezone_info, format_time_with_timezone
            event_time = obj.start_time_utc or obj.start_time_local
            if not event_time:
                return None
                
            tz_info = get_timezone_info(obj.airport.timezone, event_time)
            
            # Add formatted time displays
            if obj.start_time_local:
                tz_info['start_formatted_time'] = format_time_with_timezone(
                    obj.start_time_local, obj.airport.timezone, include_utc=True
                )
            
            if obj.end_time_local:
                tz_info['end_formatted_time'] = format_time_with_timezone(
                    obj.end_time_local, obj.airport.timezone, include_utc=True
                )
            
            return tz_info
        except Exception:
            return None

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
    trips = serializers.SerializerMethodField()
    
    class Meta:
        model = Quote
        fields = [
            'id', 'quoted_amount', 'contact', 'pickup_airport', 'dropoff_airport',
            'patient', 'payment_agreement', 'consent_for_transport', 'patient_service_agreement',
            'transactions', 'trips', 'status', 'payment_status', 'quote_pdf_status', 'aircraft_type', 'medical_team',
            'estimated_flight_time', 'includes_grounds', 'number_of_stops',
            'cruise_doctor_first_name', 'cruise_doctor_last_name', 'cruise_line', 'cruise_ship',
            'quote_pdf_email', 'created_on'
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
    
    def get_trips(self, obj):
        # Return minimal trip info to avoid circular references
        return [{
            'id': trip.id,
            'trip_number': trip.trip_number,
            'type': trip.type,
            'status': trip.status
        } for trip in obj.trips.all()]

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
            'transaction_ids', 'status', 'payment_status'
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
    trips = serializers.SerializerMethodField()
    quotes = serializers.SerializerMethodField()
    
    def get_trips(self, obj):
        trips = obj.trips.all()
        return [{'id': trip.id, 'trip_number': trip.trip_number} for trip in trips]
    
    def get_quotes(self, obj):
        quotes = obj.quotes.all()
        return [{'id': quote.id} for quote in quotes]
    
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
            'created_on',
            'trips',
            'quotes'
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
