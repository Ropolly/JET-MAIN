"""
Quote service module containing business logic for quote operations.
Extracted from models and views to follow clean architecture principles.
"""
from django.db import transaction
from django.utils import timezone
from decimal import Decimal
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

from ..models import Quote, Patient
from contacts.models import Contact
from airports.models import Airport


class QuoteService:
    """Service class for quote-related business logic."""
    
    @staticmethod
    def create_quote(
        contact_id: str,
        pickup_airport_id: str,
        dropoff_airport_id: str,
        aircraft_type: str,
        medical_team: str,
        estimated_flight_time: timedelta,
        **kwargs
    ) -> Quote:
        """
        Create a new quote with automatic pricing calculation.
        
        Args:
            contact_id: Customer contact ID
            pickup_airport_id: Origin airport ID
            dropoff_airport_id: Destination airport ID
            aircraft_type: Type of aircraft requested
            medical_team: Medical team configuration
            estimated_flight_time: Estimated flight duration
            **kwargs: Additional quote fields
            
        Returns:
            Created Quote instance
        """
        # Calculate base quote amount
        base_amount = QuoteService._calculate_base_price(
            aircraft_type, estimated_flight_time, medical_team
        )
        
        # Apply distance-based adjustments
        distance_adjustment = QuoteService._calculate_distance_adjustment(
            pickup_airport_id, dropoff_airport_id
        )
        
        quoted_amount = base_amount + distance_adjustment
        
        with transaction.atomic():
            quote = Quote.objects.create(
                contact_id=contact_id,
                pickup_airport_id=pickup_airport_id,
                dropoff_airport_id=dropoff_airport_id,
                aircraft_type=aircraft_type,
                medical_team=medical_team,
                estimated_flight_time=estimated_flight_time,
                quoted_amount=quoted_amount,
                inquiry_date=timezone.now(),
                **kwargs
            )
            
            return quote
    
    @staticmethod
    def update_quote_status(quote: Quote, new_status: str, user=None) -> Quote:
        """
        Update quote status with proper validation and logging.
        
        Args:
            quote: Quote instance
            new_status: New status value
            user: User making the change
            
        Returns:
            Updated Quote instance
            
        Raises:
            ValueError: If status transition is invalid
        """
        valid_transitions = {
            'pending': ['active', 'cancelled'],
            'active': ['completed', 'cancelled'],
            'completed': [],  # Terminal state
            'cancelled': []   # Terminal state
        }
        
        if new_status not in valid_transitions.get(quote.status, []):
            raise ValueError(
                f"Invalid status transition from {quote.status} to {new_status}"
            )
        
        quote.status = new_status
        if user:
            quote.modified_by = user
        quote.save()
        
        return quote
    
    @staticmethod
    def calculate_payment_schedule(quote: Quote) -> Dict[str, Decimal]:
        """
        Calculate payment schedule based on quote amount and type.
        
        Args:
            quote: Quote instance
            
        Returns:
            Dictionary with payment schedule
        """
        total_amount = quote.quoted_amount
        
        # Medical flights typically require 50% deposit
        if hasattr(quote, 'patient') and quote.patient:
            deposit_percentage = Decimal('0.50')
        else:
            # Charter flights require 25% deposit
            deposit_percentage = Decimal('0.25')
        
        deposit_amount = total_amount * deposit_percentage
        balance_amount = total_amount - deposit_amount
        
        return {
            'total_amount': total_amount,
            'deposit_amount': deposit_amount,
            'balance_amount': balance_amount,
            'deposit_percentage': deposit_percentage
        }
    
    @staticmethod
    def generate_quote_pdf(quote: Quote) -> str:
        """
        Generate PDF document for the quote.
        
        Args:
            quote: Quote instance
            
        Returns:
            Document ID of generated PDF
        """
        from documents.services.generation_service import DocumentGenerationService
        
        # Prepare quote data for PDF generation
        quote_data = {
            'quote_id': str(quote.id),
            'contact': quote.contact,
            'pickup_airport': quote.pickup_airport,
            'dropoff_airport': quote.dropoff_airport,
            'aircraft_type': quote.aircraft_type,
            'medical_team': quote.medical_team,
            'quoted_amount': quote.quoted_amount,
            'estimated_flight_time': quote.estimated_flight_time,
            'inquiry_date': quote.inquiry_date,
            'payment_schedule': QuoteService.calculate_payment_schedule(quote)
        }
        
        # Generate PDF using document service
        document_id = DocumentGenerationService.generate_quote_pdf(quote_data)
        
        # Update quote with generated PDF
        quote.quote_pdf_id = document_id
        quote.quote_pdf_status = 'created'
        quote.save()
        
        return document_id
    
    @staticmethod
    def _calculate_base_price(
        aircraft_type: str,
        flight_time: timedelta,
        medical_team: str
    ) -> Decimal:
        """
        Calculate base price based on aircraft and medical team.
        
        Args:
            aircraft_type: Type of aircraft
            flight_time: Flight duration
            medical_team: Medical team configuration
            
        Returns:
            Base price amount
        """
        # Base hourly rates by aircraft type
        aircraft_rates = {
            '65': Decimal('4500.00'),  # Learjet 65
            '35': Decimal('3500.00'),  # Learjet 35
            'TBD': Decimal('4000.00')  # Default rate
        }
        
        # Medical team surcharges
        medical_surcharges = {
            'RN/RN': Decimal('2000.00'),
            'RN/Paramedic': Decimal('2500.00'),
            'RN/MD': Decimal('5000.00'),
            'RN/RT': Decimal('3000.00'),
            'standard': Decimal('1000.00'),
            'full': Decimal('6000.00')
        }
        
        base_rate = aircraft_rates.get(aircraft_type, aircraft_rates['TBD'])
        medical_surcharge = medical_surcharges.get(medical_team, Decimal('0.00'))
        
        # Calculate flight hours (minimum 2 hours)
        flight_hours = max(flight_time.total_seconds() / 3600, 2)
        
        return (base_rate * Decimal(str(flight_hours))) + medical_surcharge
    
    @staticmethod
    def _calculate_distance_adjustment(
        pickup_airport_id: str,
        dropoff_airport_id: str
    ) -> Decimal:
        """
        Calculate price adjustment based on distance.
        
        Args:
            pickup_airport_id: Origin airport ID
            dropoff_airport_id: Destination airport ID
            
        Returns:
            Distance-based price adjustment
        """
        from airports.services.airport_service import AirportService
        
        pickup_airport = Airport.objects.get(id=pickup_airport_id)
        dropoff_airport = Airport.objects.get(id=dropoff_airport_id)
        
        distance = AirportService.calculate_distance(pickup_airport, dropoff_airport)
        
        # Long distance surcharge (over 1000 nautical miles)
        if distance > 1000:
            return Decimal('1000.00')
        
        # Short distance minimum charge (under 200 nautical miles)
        if distance < 200:
            return Decimal('500.00')
        
        return Decimal('0.00')


class PatientService:
    """Service class for patient-related business logic."""
    
    @staticmethod
    def create_patient_from_contact(
        contact_id: str,
        date_of_birth: datetime.date,
        nationality: str,
        passport_number: str,
        passport_expiration_date: datetime.date,
        **kwargs
    ) -> Patient:
        """
        Create a patient record from an existing contact.
        
        Args:
            contact_id: Contact ID
            date_of_birth: Patient's date of birth
            nationality: Patient's nationality
            passport_number: Passport number
            passport_expiration_date: Passport expiration date
            **kwargs: Additional patient fields
            
        Returns:
            Created Patient instance
            
        Raises:
            ValueError: If validation fails
        """
        # Validate contact exists
        contact = Contact.objects.get(id=contact_id)
        
        # Validate passport not expired
        if passport_expiration_date <= timezone.now().date():
            raise ValueError("Passport is expired")
        
        # Validate age (must be reasonable for medical transport)
        age = (timezone.now().date() - date_of_birth).days / 365.25
        if age < 0 or age > 120:
            raise ValueError("Invalid date of birth")
        
        return Patient.objects.create(
            info_id=contact_id,
            date_of_birth=date_of_birth,
            nationality=nationality,
            passport_number=passport_number,
            passport_expiration_date=passport_expiration_date,
            **kwargs
        )
    
    @staticmethod
    def validate_medical_documents(patient: Patient) -> Dict[str, bool]:
        """
        Validate that all required medical documents are present.
        
        Args:
            patient: Patient instance
            
        Returns:
            Dictionary with validation results
        """
        validation_results = {
            'passport_document': bool(patient.passport_document),
            'medical_necessity': bool(patient.letter_of_medical_necessity),
            'passport_valid': (
                patient.passport_expiration_date > timezone.now().date()
                if patient.passport_expiration_date else False
            )
        }
        
        validation_results['all_valid'] = all(validation_results.values())
        
        return validation_results
    
    @staticmethod
    def update_patient_status(patient: Patient, new_status: str, user=None) -> Patient:
        """
        Update patient status with proper validation.
        
        Args:
            patient: Patient instance
            new_status: New status value
            user: User making the change
            
        Returns:
            Updated Patient instance
            
        Raises:
            ValueError: If status transition is invalid
        """
        valid_transitions = {
            'pending': ['confirmed', 'cancelled'],
            'confirmed': ['active', 'cancelled'],
            'active': ['completed', 'cancelled'],
            'completed': [],  # Terminal state
            'cancelled': []   # Terminal state
        }
        
        if new_status not in valid_transitions.get(patient.status, []):
            raise ValueError(
                f"Invalid status transition from {patient.status} to {new_status}"
            )
        
        patient.status = new_status
        if user:
            patient.modified_by = user
        patient.save()
        
        return patient
