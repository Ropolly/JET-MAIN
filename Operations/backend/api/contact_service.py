"""
Unified Contact Creation Service

This service provides a clean, consistent way to create contact records
that can be used for patients, staff, customers, and passengers.
All passport information, birth dates, and contact details are now 
stored on the Contact model.
"""

from django.db import transaction
from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import Contact, Patient, Staff, Passenger
from typing import Dict, Any, Optional, Tuple
from datetime import date


class ContactCreationService:
    """
    Service class for creating contacts and associated records (Patient, Staff, Passenger, etc.)
    """
    
    @staticmethod
    def create_contact_with_related(
        contact_data: Dict[str, Any],
        related_type: str,
        related_data: Optional[Dict[str, Any]] = None,
        created_by=None
    ) -> Tuple[Contact, Any]:
        """
        Create a contact record along with its related record (Patient, Staff, Passenger, etc.)
        
        Args:
            contact_data: Dictionary containing contact information
            related_type: Type of related record ('patient', 'staff', 'passenger', 'customer')
            related_data: Additional data specific to the related record type
            created_by: User who is creating the record
            
        Returns:
            Tuple of (Contact instance, Related instance)
            
        Raises:
            ValidationError: If data validation fails
        """
        if related_data is None:
            related_data = {}
            
        with transaction.atomic():
            # Validate and create contact
            contact = ContactCreationService._create_contact(contact_data, created_by)
            
            # Create related record
            related_instance = None
            if related_type == 'patient':
                related_instance = ContactCreationService._create_patient(contact, related_data, created_by)
            elif related_type == 'staff':
                related_instance = ContactCreationService._create_staff(contact, related_data, created_by)
            elif related_type == 'passenger':
                related_instance = ContactCreationService._create_passenger(contact, related_data, created_by)
            elif related_type == 'customer':
                # For customers, we just need the contact record
                related_instance = contact
            else:
                raise ValidationError(f"Unknown related type: {related_type}")
                
            return contact, related_instance
    
    @staticmethod
    def _create_contact(contact_data: Dict[str, Any], created_by=None) -> Contact:
        """
        Create and validate a Contact record
        """
        # Validate required fields
        ContactCreationService._validate_contact_data(contact_data)
        
        # Create contact instance
        contact = Contact(
            # Personal Information
            first_name=contact_data.get('first_name', '').strip(),
            last_name=contact_data.get('last_name', '').strip(),
            business_name=contact_data.get('business_name', '').strip(),
            
            # Contact Information
            email=contact_data.get('email', '').strip(),
            phone=contact_data.get('phone', '').strip(),
            
            # Address Information
            address_line1=contact_data.get('address_line1', '').strip(),
            address_line2=contact_data.get('address_line2', '').strip(),
            city=contact_data.get('city', '').strip(),
            state=contact_data.get('state', '').strip(),
            zip=contact_data.get('zip', '').strip(),
            country=contact_data.get('country', '').strip(),
            
            # Personal Details (now on Contact table)
            nationality=contact_data.get('nationality', '').strip(),
            date_of_birth=contact_data.get('date_of_birth'),
            passport_number=contact_data.get('passport_number', '').strip(),
            passport_expiration_date=contact_data.get('passport_expiration_date'),
            
            # Audit fields
            created_by=created_by,
            status=contact_data.get('status', 'active')
        )
        
        # Validate and save
        contact.full_clean()
        contact.save()
        
        return contact
    
    @staticmethod
    def _create_patient(contact: Contact, patient_data: Dict[str, Any], created_by=None) -> Patient:
        """
        Create a Patient record linked to the Contact
        """
        patient = Patient(
            info=contact,
            special_instructions=patient_data.get('special_instructions', '').strip(),
            bed_at_origin=patient_data.get('bed_at_origin', False),
            bed_at_destination=patient_data.get('bed_at_destination', False),
            status=patient_data.get('status', 'pending'),
            created_by=created_by,
            
            # Note: These fields are now deprecated and will be removed in future migration
            # The data should come from contact.date_of_birth, contact.nationality, etc.
            date_of_birth=contact.date_of_birth or date.today(),
            nationality=contact.nationality or 'Unknown',
            passport_number=contact.passport_number or '',
            passport_expiration_date=contact.passport_expiration_date or date.today(),
        )
        
        patient.full_clean()
        patient.save()
        
        return patient
    
    @staticmethod
    def _create_staff(contact: Contact, staff_data: Dict[str, Any], created_by=None) -> Staff:
        """
        Create a Staff record linked to the Contact
        """
        # Check if staff already exists for this contact
        if Staff.objects.filter(contact=contact).exists():
            raise ValidationError("Staff record already exists for this contact")
            
        staff = Staff(
            contact=contact,
            active=staff_data.get('active', True),
            notes=staff_data.get('notes', '').strip(),
            created_by=created_by
        )
        
        staff.full_clean()
        staff.save()
        
        return staff
    
    @staticmethod
    def _create_passenger(contact: Contact, passenger_data: Dict[str, Any], created_by=None) -> Passenger:
        """
        Create a Passenger record linked to the Contact
        """
        passenger = Passenger(
            info=contact,
            contact_number=passenger_data.get('contact_number', '').strip(),
            notes=passenger_data.get('notes', '').strip(),
            status=passenger_data.get('status', 'active'),
            created_by=created_by,
            
            # Note: These fields are now deprecated and will be removed in future migration
            # The data should come from contact.date_of_birth, contact.nationality, etc.
            date_of_birth=contact.date_of_birth,
            nationality=contact.nationality or '',
            passport_number=contact.passport_number or '',
            passport_expiration_date=contact.passport_expiration_date,
        )
        
        passenger.full_clean()
        passenger.save()
        
        return passenger
    
    @staticmethod
    def _validate_contact_data(contact_data: Dict[str, Any]):
        """
        Validate contact data before creation
        """
        # Check that either personal name or business name is provided
        first_name = contact_data.get('first_name', '').strip()
        last_name = contact_data.get('last_name', '').strip()
        business_name = contact_data.get('business_name', '').strip()
        
        if not first_name and not last_name and not business_name:
            raise ValidationError("Either first/last name or business name is required")
        
        # Validate email format if provided
        email = contact_data.get('email', '').strip()
        if email and '@' not in email:
            raise ValidationError("Invalid email format")
        
        # Validate passport expiration is after birth date if both provided
        birth_date = contact_data.get('date_of_birth')
        passport_expiration = contact_data.get('passport_expiration_date')
        
        if birth_date and passport_expiration and passport_expiration <= birth_date:
            raise ValidationError("Passport expiration date must be after date of birth")
    
    @staticmethod
    def update_contact_and_related(
        contact: Contact,
        contact_data: Dict[str, Any],
        related_instance: Any = None,
        related_data: Optional[Dict[str, Any]] = None
    ) -> Tuple[Contact, Any]:
        """
        Update existing contact and related record
        """
        with transaction.atomic():
            # Update contact fields
            for field, value in contact_data.items():
                if hasattr(contact, field):
                    if isinstance(value, str):
                        value = value.strip()
                    setattr(contact, field, value)
            
            contact.full_clean()
            contact.save()
            
            # Update related record if provided
            if related_instance and related_data:
                for field, value in related_data.items():
                    if hasattr(related_instance, field):
                        if isinstance(value, str):
                            value = value.strip()
                        setattr(related_instance, field, value)
                
                related_instance.full_clean()
                related_instance.save()
            
            return contact, related_instance


class ContactCreationSerializer(serializers.Serializer):
    """
    Serializer for unified contact creation requests
    """
    # Contact data
    first_name = serializers.CharField(max_length=100, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=100, required=False, allow_blank=True)
    business_name = serializers.CharField(max_length=255, required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    
    # Address fields
    address_line1 = serializers.CharField(max_length=255, required=False, allow_blank=True)
    address_line2 = serializers.CharField(max_length=255, required=False, allow_blank=True)
    city = serializers.CharField(max_length=100, required=False, allow_blank=True)
    state = serializers.CharField(max_length=100, required=False, allow_blank=True)
    zip = serializers.CharField(max_length=20, required=False, allow_blank=True)
    country = serializers.CharField(max_length=100, required=False, allow_blank=True)
    
    # Personal details (now on Contact table)
    nationality = serializers.CharField(max_length=100, required=False, allow_blank=True)
    date_of_birth = serializers.DateField(required=False, allow_null=True)
    passport_number = serializers.CharField(max_length=100, required=False, allow_blank=True)
    passport_expiration_date = serializers.DateField(required=False, allow_null=True)
    
    # Related record type and data
    related_type = serializers.ChoiceField(
        choices=['patient', 'staff', 'passenger', 'customer'],
        required=True
    )
    related_data = serializers.JSONField(required=False, default=dict)
    
    def validate(self, data):
        # Ensure either personal or business name is provided
        first_name = data.get('first_name', '').strip()
        last_name = data.get('last_name', '').strip()
        business_name = data.get('business_name', '').strip()
        
        if not first_name and not last_name and not business_name:
            raise serializers.ValidationError(
                "Either first/last name or business name is required"
            )
        
        return data
    
    def create(self, validated_data):
        # Extract related data
        related_type = validated_data.pop('related_type')
        related_data = validated_data.pop('related_data', {})
        
        # Get user from context
        created_by = self.context.get('request').user if self.context.get('request') else None
        
        # Create contact and related record
        contact, related_instance = ContactCreationService.create_contact_with_related(
            contact_data=validated_data,
            related_type=related_type,
            related_data=related_data,
            created_by=created_by
        )
        
        return {
            'contact': contact,
            'related_instance': related_instance,
            'related_type': related_type
        }