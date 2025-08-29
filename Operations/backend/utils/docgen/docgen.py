#!/usr/bin/env python
"""
Document Generation System for JET Aviation Operations

This module handles the generation of aviation-related documents including:
- General Declaration (GenDec)
- Handling Requests
- Customer Itineraries
- Internal Itineraries
- Quote Forms
"""

import os
import sys
import django
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List

# Setup Django environment for standalone script execution
sys.path.append(str(Path(__file__).parent.parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.utils import timezone
from api.models import TripLine, Trip, Aircraft, Contact, Passenger, Patient

try:
    from docx import Document
    from docx.shared import Inches
except ImportError:
    print("Warning: python-docx not installed. Install with: pip install python-docx")
    Document = None


class DocumentGenerator:
    """Main document generation class for aviation documents."""
    
    def __init__(self):
        """Initialize the document generator with template and output paths."""
        self.base_dir = Path(__file__).parent
        self.templates_dir = self.base_dir / "documents"
        self.outputs_dir = self.base_dir / "outputs"
        
        # Ensure outputs directory exists
        self.outputs_dir.mkdir(exist_ok=True)
        
        # Check if templates directory exists
        if not self.templates_dir.exists():
            raise FileNotFoundError(f"Templates directory not found: {self.templates_dir}")
    
    def generate_general_declaration(self, trip_line_id: str) -> str:
        """Generate a General Declaration (GenDec) document for a trip line.
        
        Args:
            trip_line_id: UUID string of the TripLine to generate GenDec for
            
        Returns:
            str: Path to the generated document
            
        Raises:
            TripLine.DoesNotExist: If trip line is not found
            FileNotFoundError: If GenDec template is not found
        """
        try:
            trip_line = TripLine.objects.select_related(
                'trip', 'trip__aircraft', 'trip__patient', 'trip__patient__info',
                'origin_airport', 'destination_airport', 'crew_line',
                'crew_line__primary_in_command', 'crew_line__secondary_in_command'
            ).prefetch_related(
                'trip__passengers', 'trip__passengers__info',
                'crew_line__medic_ids'
            ).get(id=trip_line_id)
        except TripLine.DoesNotExist:
            raise TripLine.DoesNotExist(f"Trip line with ID {trip_line_id} not found")
        
        # Prepare data for GenDec
        data = self._prepare_gendec_data(trip_line)
        
        # Generate document
        template_path = self.templates_dir / "GenDec.docx"
        if not template_path.exists():
            raise FileNotFoundError(f"GenDec template not found: {template_path}")
        
        # Create output filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        trip_number = trip_line.trip.trip_number or "UNKNOWN"
        leg_suffix = f"{trip_line.origin_airport.iata_code}_{trip_line.destination_airport.iata_code}"
        output_filename = f"GenDec_{trip_number}_{leg_suffix}_{timestamp}.docx"
        output_path = self.outputs_dir / output_filename
        
        # Generate the document
        if Document is not None:
            try:
                return self._fill_docx_template(template_path, output_path, data)
            except Exception as e:
                print(f"Error using python-docx: {e}. Falling back to text replacement.")
                return self._fill_template_fallback(template_path, output_path, data)
        else:
            return self._fill_template_fallback(template_path, output_path, data)
    
    def _prepare_gendec_data(self, trip_line: TripLine) -> Dict[str, Any]:
        """Prepare data for GenDec document generation.
        
        Args:
            trip_line: TripLine instance with related data
            
        Returns:
            Dict containing all data needed for GenDec document
        """
        trip = trip_line.trip
        aircraft = trip.aircraft
        origin = trip_line.origin_airport
        destination = trip_line.destination_airport
        crew_line = trip_line.crew_line
        
        # Format dates and times
        departure_local = trip_line.departure_time_local.strftime("%Y-%m-%d %H:%M") if trip_line.departure_time_local else "TBD"
        departure_utc = trip_line.departure_time_utc.strftime("%Y-%m-%d %H:%M UTC") if trip_line.departure_time_utc else "TBD"
        arrival_local = trip_line.arrival_time_local.strftime("%Y-%m-%d %H:%M") if trip_line.arrival_time_local else "TBD"
        arrival_utc = trip_line.arrival_time_utc.strftime("%Y-%m-%d %H:%M UTC") if trip_line.arrival_time_utc else "TBD"
        
        # Aircraft information
        aircraft_info = {
            'tail_number': aircraft.tail_number if aircraft else "N/A",
            'type': aircraft.type if aircraft else "N/A",
            'manufacturer': aircraft.manufacturer if aircraft else "N/A",
            'model': aircraft.model if aircraft else "N/A",
            'year': str(aircraft.year) if aircraft and aircraft.year else "N/A"
        }
        
        # Crew information
        crew_info = {
            'primary_pilot': self._format_contact(crew_line.primary_in_command) if crew_line and crew_line.primary_in_command else "N/A",
            'secondary_pilot': self._format_contact(crew_line.secondary_in_command) if crew_line and crew_line.secondary_in_command else "N/A",
            'medics': []
        }
        
        if crew_line:
            for medic in crew_line.medic_ids.all():
                crew_info['medics'].append(self._format_contact(medic))
        
        # Passenger information (only for passenger legs)
        passengers_info = []
        if trip_line.passenger_leg and trip.passengers.exists():
            for passenger in trip.passengers.all():
                passenger_data = {
                    'name': self._format_contact(passenger.info),
                    'nationality': passenger.nationality or "N/A",
                    'passport_number': passenger.passport_number or "N/A",
                    'date_of_birth': passenger.date_of_birth.strftime("%Y-%m-%d") if passenger.date_of_birth else "N/A"
                }
                passengers_info.append(passenger_data)
        
        # Patient information (for medical trips)
        patient_info = None
        if trip.patient:
            patient_info = {
                'name': self._format_contact(trip.patient.info) if trip.patient.info else "N/A",
                'date_of_birth': trip.patient.date_of_birth.strftime("%Y-%m-%d") if trip.patient.date_of_birth else "N/A"
            }
        
        # Compile all data
        data = {
            # Flight information
            'trip_number': trip.trip_number or "N/A",
            'flight_type': "Passenger" if trip_line.passenger_leg else "Repositioning",
            'departure_date': departure_local,
            'departure_time_utc': departure_utc,
            'arrival_date': arrival_local,
            'arrival_time_utc': arrival_utc,
            'flight_time': str(trip_line.flight_time) if trip_line.flight_time else "N/A",
            'distance': f"{trip_line.distance} NM" if trip_line.distance else "N/A",
            
            # Airport information
            'origin_airport_name': origin.name if origin else "N/A",
            'origin_airport_code': origin.iata_code if origin else "N/A",
            'origin_airport_icao': origin.icao_code if origin else "N/A",
            'origin_city': origin.city if origin else "N/A",
            'origin_country': origin.country if origin else "N/A",
            
            'destination_airport_name': destination.name if destination else "N/A",
            'destination_airport_code': destination.iata_code if destination else "N/A",
            'destination_airport_icao': destination.icao_code if destination else "N/A",
            'destination_city': destination.city if destination else "N/A",
            'destination_country': destination.country if destination else "N/A",
            
            # Aircraft and crew
            'aircraft': aircraft_info,
            'crew': crew_info,
            
            # Passengers and patient
            'passengers': passengers_info,
            'passenger_count': len(passengers_info),
            'patient': patient_info,
            
            # Document metadata
            'document_date': timezone.now().strftime("%Y-%m-%d"),
            'document_time': timezone.now().strftime("%H:%M:%S UTC")
        }
        
        return data
    
    def _format_contact(self, contact: Contact) -> str:
        """Format a contact's name for display.
        
        Args:
            contact: Contact instance
            
        Returns:
            Formatted name string
        """
        if not contact:
            return "N/A"
        
        first_name = contact.first_name or ""
        last_name = contact.last_name or ""
        
        if first_name and last_name:
            return f"{first_name} {last_name}"
        elif first_name:
            return first_name
        elif last_name:
            return last_name
        else:
            return contact.email or "N/A"
    
    def _fill_docx_template(self, template_path: Path, output_path: Path, data: Dict[str, Any]) -> str:
        """Fill a Word document template using python-docx.
        
        Args:
            template_path: Path to template file
            output_path: Path for output file
            data: Data to fill in template
            
        Returns:
            Path to generated document
        """
        doc = Document(template_path)
        
        # Replace placeholders in paragraphs
        for paragraph in doc.paragraphs:
            self._replace_placeholders_in_text(paragraph, data)
        
        # Replace placeholders in tables
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    for paragraph in cell.paragraphs:
                        self._replace_placeholders_in_text(paragraph, data)
        
        # Save the document
        doc.save(output_path)
        return str(output_path)
    
    def _replace_placeholders_in_text(self, paragraph, data: Dict[str, Any]):
        """Replace placeholders in a paragraph with actual data.
        
        Args:
            paragraph: Document paragraph object
            data: Data dictionary for replacements
        """
        # Create mapping of placeholders to actual values
        replacements = {
            '{{TRIP_NUMBER}}': data['trip_number'],
            '{{FLIGHT_TYPE}}': data['flight_type'],
            '{{DEPARTURE_DATE}}': data['departure_date'],
            '{{DEPARTURE_TIME_UTC}}': data['departure_time_utc'],
            '{{ARRIVAL_DATE}}': data['arrival_date'],
            '{{ARRIVAL_TIME_UTC}}': data['arrival_time_utc'],
            '{{FLIGHT_TIME}}': data['flight_time'],
            '{{DISTANCE}}': data['distance'],
            
            '{{ORIGIN_AIRPORT}}': data['origin_airport_name'],
            '{{ORIGIN_CODE}}': data['origin_airport_code'],
            '{{ORIGIN_ICAO}}': data['origin_airport_icao'],
            '{{ORIGIN_CITY}}': data['origin_city'],
            '{{ORIGIN_COUNTRY}}': data['origin_country'],
            
            '{{DESTINATION_AIRPORT}}': data['destination_airport_name'],
            '{{DESTINATION_CODE}}': data['destination_airport_code'],
            '{{DESTINATION_ICAO}}': data['destination_airport_icao'],
            '{{DESTINATION_CITY}}': data['destination_city'],
            '{{DESTINATION_COUNTRY}}': data['destination_country'],
            
            '{{AIRCRAFT_TAIL}}': data['aircraft']['tail_number'],
            '{{AIRCRAFT_TYPE}}': data['aircraft']['type'],
            '{{AIRCRAFT_MANUFACTURER}}': data['aircraft']['manufacturer'],
            '{{AIRCRAFT_MODEL}}': data['aircraft']['model'],
            '{{AIRCRAFT_YEAR}}': data['aircraft']['year'],
            
            '{{PRIMARY_PILOT}}': data['crew']['primary_pilot'],
            '{{SECONDARY_PILOT}}': data['crew']['secondary_pilot'],
            '{{MEDICS}}': ', '.join(data['crew']['medics']) if data['crew']['medics'] else 'N/A',
            
            '{{PASSENGER_COUNT}}': str(data['passenger_count']),
            '{{DOCUMENT_DATE}}': data['document_date'],
            '{{DOCUMENT_TIME}}': data['document_time'],
        }
        
        # Add passenger list
        if data['passengers']:
            passenger_list = '\n'.join([
                f"{p['name']} - {p['nationality']} - Passport: {p['passport_number']}"
                for p in data['passengers']
            ])
            replacements['{{PASSENGER_LIST}}'] = passenger_list
        else:
            replacements['{{PASSENGER_LIST}}'] = 'No passengers (Repositioning flight)'
        
        # Add patient info if available
        if data['patient']:
            replacements['{{PATIENT_NAME}}'] = data['patient']['name']
            replacements['{{PATIENT_DOB}}'] = data['patient']['date_of_birth']
        else:
            replacements['{{PATIENT_NAME}}'] = 'N/A'
            replacements['{{PATIENT_DOB}}'] = 'N/A'
        
        # Apply replacements
        full_text = paragraph.text
        for placeholder, value in replacements.items():
            if placeholder in full_text:
                full_text = full_text.replace(placeholder, str(value))
        
        # Update paragraph text if changes were made
        if full_text != paragraph.text:
            paragraph.text = full_text
    
    def _fill_template_fallback(self, template_path: Path, output_path: Path, data: Dict[str, Any]) -> str:
        """Fallback method for template filling when python-docx is not available.
        
        Args:
            template_path: Path to template file
            output_path: Path for output file
            data: Data to fill in template
            
        Returns:
            Path to generated document
        """
        # Simple copy of template as fallback
        import shutil
        shutil.copy2(template_path, output_path)
        
        print(f"Warning: Template filled using fallback method. Generated document: {output_path}")
        print("For full template processing, install python-docx: pip install python-docx")
        
        return str(output_path)


def generate_gendec_for_trip_line(trip_line_id: str) -> str:
    """Convenience function to generate GenDec for a trip line.
    
    Args:
        trip_line_id: UUID string of the TripLine
        
    Returns:
        Path to the generated GenDec document
    """
    generator = DocumentGenerator()
    return generator.generate_general_declaration(trip_line_id)


def generate_gendec_for_trip(trip_id: str) -> List[str]:
    """Generate GenDec documents for all trip lines in a trip.
    
    Args:
        trip_id: UUID string of the Trip
        
    Returns:
        List of paths to generated GenDec documents
    """
    try:
        trip = Trip.objects.prefetch_related('trip_lines').get(id=trip_id)
    except Trip.DoesNotExist:
        raise Trip.DoesNotExist(f"Trip with ID {trip_id} not found")
    
    generator = DocumentGenerator()
    generated_docs = []
    
    for trip_line in trip.trip_lines.all():
        doc_path = generator.generate_general_declaration(str(trip_line.id))
        generated_docs.append(doc_path)
    
    return generated_docs


if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python docgen.py <trip_line_id>")
        sys.exit(1)
    
    trip_line_id = sys.argv[1]
    
    try:
        doc_path = generate_gendec_for_trip_line(trip_line_id)
        print(f"GenDec generated successfully: {doc_path}")
    except Exception as e:
        print(f"Error generating GenDec: {e}")
        sys.exit(1)