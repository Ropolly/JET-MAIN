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
        read_only_fields = ['is_staff']

# Base serializers
class ModificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modification
        fields = '__all__'

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = '__all__'

# Contact and location serializers
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

class FBOSerializer(serializers.ModelSerializer):
    class Meta:
        model = FBO
        fields = '__all__'

class GroundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ground
        fields = '__all__'

class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = '__all__'

# Document serializer
class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'filename', 'flag', 'created_on']

class DocumentUploadSerializer(serializers.ModelSerializer):
    content = serializers.FileField()
    
    class Meta:
        model = Document
        fields = ['id', 'filename', 'content', 'flag']

# Aircraft serializer
class AircraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aircraft
        fields = '__all__'

# Transaction serializer
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

# Agreement serializer
class AgreementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agreement
        fields = '__all__'

# Patient serializer
class PatientSerializer(serializers.ModelSerializer):
    info = ContactSerializer(read_only=True)
    info_id = serializers.PrimaryKeyRelatedField(
        queryset=Contact.objects.all(),
        source='info',
        write_only=True
    )
    
    class Meta:
        model = Patient
        fields = '__all__'

# Quote serializer
class QuoteSerializer(serializers.ModelSerializer):
    contact = ContactSerializer(source='contact_id', read_only=True)
    
    class Meta:
        model = Quote
        fields = '__all__'

# Passenger serializer
class PassengerSerializer(serializers.ModelSerializer):
    info = ContactSerializer(read_only=True)
    
    class Meta:
        model = Passenger
        fields = '__all__'

# Crew Line serializer
class CrewLineSerializer(serializers.ModelSerializer):
    primary_in_command = ContactSerializer(source='primary_in_command_id', read_only=True)
    secondary_in_command = ContactSerializer(source='secondary_in_command_id', read_only=True)
    medics = ContactSerializer(source='medic_ids', many=True, read_only=True)
    
    class Meta:
        model = CrewLine
        fields = '__all__'

# Trip serializer
class TripLineSerializer(serializers.ModelSerializer):
    origin_airport = AirportSerializer(source='origin_airport_id', read_only=True)
    destination_airport = AirportSerializer(source='destination_airport_id', read_only=True)
    crew_line = CrewLineSerializer(source='crew_line_id', read_only=True)
    
    class Meta:
        model = TripLine
        fields = '__all__'

class TripSerializer(serializers.ModelSerializer):
    quote = QuoteSerializer(source='quote_id', read_only=True)
    patient = PatientSerializer(source='patient_id', read_only=True)
    aircraft = AircraftSerializer(source='aircraft_id', read_only=True)
    trip_lines = TripLineSerializer(many=True, read_only=True)
    passengers_data = PassengerSerializer(source='passengers', many=True, read_only=True)
    
    class Meta:
        model = Trip
        fields = '__all__'
