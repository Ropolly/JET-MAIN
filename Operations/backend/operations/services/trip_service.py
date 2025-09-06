"""
Trip service module containing business logic for trip operations.
Extracted from models and views to follow clean architecture principles.
"""
from django.db import transaction
from django.utils import timezone
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta

from ..models import Trip, TripLine, TripEvent, CrewLine
from contacts.models import Contact
from airports.models import Airport
from aircraft.models import Aircraft


class TripService:
    """Service class for trip-related business logic."""
    
    @staticmethod
    def create_trip(
        trip_number: str,
        trip_type: str,
        aircraft_id: Optional[str] = None,
        quote_id: Optional[str] = None,
        patient_id: Optional[str] = None,
        **kwargs
    ) -> Trip:
        """
        Create a new trip with proper validation and business rules.
        
        Args:
            trip_number: Unique trip identifier
            trip_type: Type of trip (medical, charter, etc.)
            aircraft_id: Optional aircraft assignment
            quote_id: Optional related quote
            patient_id: Optional patient for medical trips
            **kwargs: Additional trip fields
            
        Returns:
            Created Trip instance
            
        Raises:
            ValueError: If business rules are violated
        """
        # Validate trip number uniqueness
        if Trip.objects.filter(trip_number=trip_number).exists():
            raise ValueError(f"Trip number {trip_number} already exists")
        
        # Validate medical trips have patients
        if trip_type == 'medical' and not patient_id:
            raise ValueError("Medical trips must have an associated patient")
        
        with transaction.atomic():
            trip = Trip.objects.create(
                trip_number=trip_number,
                type=trip_type,
                aircraft_id=aircraft_id,
                quote_id=quote_id,
                patient_id=patient_id,
                **kwargs
            )
            
            # Auto-generate trip number if not provided
            if not trip_number:
                trip.trip_number = TripService._generate_trip_number(trip.type)
                trip.save()
            
            return trip
    
    @staticmethod
    def add_trip_line(
        trip: Trip,
        origin_airport_id: str,
        destination_airport_id: str,
        departure_time_local: datetime,
        arrival_time_local: datetime,
        crew_line_id: Optional[str] = None,
        **kwargs
    ) -> TripLine:
        """
        Add a flight leg to a trip with proper timezone handling.
        
        Args:
            trip: Trip instance
            origin_airport_id: Origin airport ID
            destination_airport_id: Destination airport ID
            departure_time_local: Local departure time
            arrival_time_local: Local arrival time
            crew_line_id: Optional crew assignment
            **kwargs: Additional trip line fields
            
        Returns:
            Created TripLine instance
        """
        from airports.services.airport_service import AirportService
        
        # Get airports for timezone conversion
        origin_airport = Airport.objects.get(id=origin_airport_id)
        destination_airport = Airport.objects.get(id=destination_airport_id)
        
        # Convert local times to UTC
        departure_time_utc = AirportService.convert_to_utc(
            departure_time_local, origin_airport.timezone
        )
        arrival_time_utc = AirportService.convert_to_utc(
            arrival_time_local, destination_airport.timezone
        )
        
        # Calculate flight time and distance
        flight_time = arrival_time_utc - departure_time_utc
        distance = AirportService.calculate_distance(origin_airport, destination_airport)
        
        return TripLine.objects.create(
            trip=trip,
            origin_airport_id=origin_airport_id,
            destination_airport_id=destination_airport_id,
            departure_time_local=departure_time_local,
            departure_time_utc=departure_time_utc,
            arrival_time_local=arrival_time_local,
            arrival_time_utc=arrival_time_utc,
            flight_time=flight_time,
            distance=distance,
            crew_line_id=crew_line_id,
            **kwargs
        )
    
    @staticmethod
    def add_crew_change_event(
        trip: Trip,
        airport_id: str,
        new_crew_line_id: str,
        event_time_local: datetime,
        notes: Optional[str] = None
    ) -> TripEvent:
        """
        Add a crew change event to a trip.
        
        Args:
            trip: Trip instance
            airport_id: Airport where crew change occurs
            new_crew_line_id: New crew assignment
            event_time_local: Local time of crew change
            notes: Optional notes about the crew change
            
        Returns:
            Created TripEvent instance
        """
        from airports.services.airport_service import AirportService
        
        airport = Airport.objects.get(id=airport_id)
        event_time_utc = AirportService.convert_to_utc(
            event_time_local, airport.timezone
        )
        
        return TripEvent.objects.create(
            trip=trip,
            airport_id=airport_id,
            event_type='CREW_CHANGE',
            start_time_local=event_time_local,
            start_time_utc=event_time_utc,
            crew_line_id=new_crew_line_id,
            notes=notes
        )
    
    @staticmethod
    def calculate_trip_duration(trip: Trip) -> Optional[timedelta]:
        """
        Calculate total trip duration from first departure to last arrival.
        
        Args:
            trip: Trip instance
            
        Returns:
            Total trip duration or None if no trip lines
        """
        trip_lines = trip.trip_lines.order_by('departure_time_utc')
        
        if not trip_lines.exists():
            return None
        
        first_departure = trip_lines.first().departure_time_utc
        last_arrival = trip_lines.last().arrival_time_utc
        
        return last_arrival - first_departure
    
    @staticmethod
    def get_trip_timeline(trip: Trip) -> List[Dict[str, Any]]:
        """
        Get chronological timeline of all trip events and flight legs.
        
        Args:
            trip: Trip instance
            
        Returns:
            List of timeline events sorted by time
        """
        timeline = []
        
        # Add trip lines
        for trip_line in trip.trip_lines.all():
            timeline.append({
                'type': 'flight',
                'time_utc': trip_line.departure_time_utc,
                'time_local': trip_line.departure_time_local,
                'event': 'departure',
                'location': trip_line.origin_airport,
                'details': trip_line
            })
            timeline.append({
                'type': 'flight',
                'time_utc': trip_line.arrival_time_utc,
                'time_local': trip_line.arrival_time_local,
                'event': 'arrival',
                'location': trip_line.destination_airport,
                'details': trip_line
            })
        
        # Add trip events
        for event in trip.events.all():
            timeline.append({
                'type': 'event',
                'time_utc': event.start_time_utc,
                'time_local': event.start_time_local,
                'event': event.event_type.lower(),
                'location': event.airport,
                'details': event
            })
        
        # Sort by UTC time
        timeline.sort(key=lambda x: x['time_utc'])
        
        return timeline
    
    @staticmethod
    def _generate_trip_number(trip_type: str) -> str:
        """
        Generate a unique trip number based on type and date.
        
        Args:
            trip_type: Type of trip
            
        Returns:
            Generated trip number
        """
        today = timezone.now().date()
        prefix_map = {
            'medical': 'MED',
            'charter': 'CHR',
            'part_91': 'P91',
            'maintenance': 'MNT',
            'other': 'OTH'
        }
        
        prefix = prefix_map.get(trip_type, 'TRP')
        date_str = today.strftime('%Y%m%d')
        
        # Find next available number for today
        existing_count = Trip.objects.filter(
            trip_number__startswith=f"{prefix}{date_str}",
            created_on__date=today
        ).count()
        
        return f"{prefix}{date_str}{existing_count + 1:03d}"


class CrewService:
    """Service class for crew-related business logic."""
    
    @staticmethod
    def create_crew_line(
        primary_pic_id: str,
        secondary_sic_id: str,
        medic_ids: Optional[List[str]] = None
    ) -> CrewLine:
        """
        Create a crew line with validation.
        
        Args:
            primary_pic_id: Primary pilot in command contact ID
            secondary_sic_id: Secondary pilot in command contact ID
            medic_ids: Optional list of medic contact IDs
            
        Returns:
            Created CrewLine instance
            
        Raises:
            ValueError: If crew validation fails
        """
        # Validate pilots are different
        if primary_pic_id == secondary_sic_id:
            raise ValueError("Primary and secondary pilots must be different")
        
        # Validate contacts exist and are staff
        primary_contact = Contact.objects.get(id=primary_pic_id)
        secondary_contact = Contact.objects.get(id=secondary_sic_id)
        
        if not hasattr(primary_contact, 'staff') or not primary_contact.staff.active:
            raise ValueError("Primary pilot must be active staff")
        
        if not hasattr(secondary_contact, 'staff') or not secondary_contact.staff.active:
            raise ValueError("Secondary pilot must be active staff")
        
        crew_line = CrewLine.objects.create(
            primary_in_command_id=primary_pic_id,
            secondary_in_command_id=secondary_sic_id
        )
        
        if medic_ids:
            crew_line.medic_ids.set(medic_ids)
        
        return crew_line
    
    @staticmethod
    def validate_crew_availability(
        crew_line: CrewLine,
        start_time: datetime,
        end_time: datetime
    ) -> Dict[str, bool]:
        """
        Check if crew members are available for the given time period.
        
        Args:
            crew_line: CrewLine instance
            start_time: Start of duty period
            end_time: End of duty period
            
        Returns:
            Dictionary with availability status for each crew member
        """
        availability = {}
        
        # Check primary pilot
        primary_conflicts = TripLine.objects.filter(
            crew_line__primary_in_command=crew_line.primary_in_command,
            departure_time_utc__lt=end_time,
            arrival_time_utc__gt=start_time
        ).exists()
        availability['primary_available'] = not primary_conflicts
        
        # Check secondary pilot
        secondary_conflicts = TripLine.objects.filter(
            crew_line__secondary_in_command=crew_line.secondary_in_command,
            departure_time_utc__lt=end_time,
            arrival_time_utc__gt=start_time
        ).exists()
        availability['secondary_available'] = not secondary_conflicts
        
        # Check medics
        for medic in crew_line.medic_ids.all():
            medic_conflicts = TripLine.objects.filter(
                crew_line__medic_ids=medic,
                departure_time_utc__lt=end_time,
                arrival_time_utc__gt=start_time
            ).exists()
            availability[f'medic_{medic.id}_available'] = not medic_conflicts
        
        return availability
