"""
Enhanced General Declaration PDF Generation Module
Handles proper filling of gen_dec.pdf with correct member titles and data
"""

from dataclasses import dataclass
from typing import List, Dict, Any
from PyPDF2 import PdfReader, PdfWriter
import os


def fill_form(original, output, data):
    """Fill PDF form fields using PyPDF2"""
    try:
        reader = PdfReader(original, strict=False)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        for page in writer.pages:
            writer.update_page_form_field_values(page, data)

        with open(output, "wb") as f:
            writer.write(f)
        return True
    except Exception as e:
        print(f"PyPDF2 form filling failed: {e}")
        return False


@dataclass
class GenDecMember:
    """Represents a member (crew or passenger) for general declaration"""
    name: str
    title: str  # "PIC", "SIC", "MED", or "PAX"
    nationality: str = ""
    passport_num: str = ""
    
    def __str__(self):
        return f"{self.name} ({self.title})"


@dataclass
class Airport:
    icao: str
    city: str
    country: str


@dataclass
class GenDecData:
    """Enhanced data class for General Declaration with proper member handling"""
    owner: str                 # Owner/Operator
    tail_num: str              # Marks of Nationality
    flight_no: str
    date: str
    depart: Airport
    arrive: Airport
    members: List[GenDecMember]
    
    @property
    def total_occupants(self) -> int:
        """Total number of occupants"""
        return len(self.members)
    
    @property
    def pic_count(self) -> int:
        """Number of PICs"""
        return len([m for m in self.members if m.title == "PIC"])
    
    @property
    def sic_count(self) -> int:
        """Number of SICs"""
        return len([m for m in self.members if m.title == "SIC"])
    
    @property
    def med_count(self) -> int:
        """Number of medical crew"""
        return len([m for m in self.members if m.title == "MED"])
    
    @property
    def pax_count(self) -> int:
        """Number of passengers (including patients)"""
        return len([m for m in self.members if m.title == "PAX"])


def populate_gen_dec_pdf_enhanced(input_pdf_path: str, output_pdf_path: str, data: GenDecData) -> bool:
    """
    Enhanced function to populate gen_dec.pdf with proper field mapping
    
    Args:
        input_pdf_path: Path to the template PDF
        output_pdf_path: Path where the filled PDF will be saved
        data: GenDecData instance with member information
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Create field mapping for the PDF
        field_mapping = {
            # Aircraft information
            "OwnerorOperator[0]": data.owner,
            "MarksofNationality[0]": data.tail_num,
            "flightnumber[0]": data.flight_no,
            "Date[0]": data.date,
            "departurefrom[0]": f"{data.depart.city}, {data.depart.country} ({data.depart.icao})",
            "arrivaat[0]": f"{data.arrive.city}, {data.arrive.country} ({data.arrive.icao})",
            
            # Origin location with total occupants
            "place1[0]": f"{data.depart.city}, {data.depart.country}",
            "totalnumber1[0]": str(data.total_occupants),
            
            # Movement data - all embarking at origin for medical transport
            "embarking[0]": str(data.total_occupants),
            "disembarking[0]": "0",
            "throughonsameflight[0]": "0",
            "throughonsameflight2[0]": "0",
            
            # Additional information
            "declaration1[0]": f"Medical transport flight with {data.total_occupants} occupants",
            "details1[0]": f"Crew: PIC({data.pic_count}), SIC({data.sic_count}), MED({data.med_count}), PAX({data.pax_count})",
            "other1[0]": f"Members: {', '.join([str(m) for m in data.members[:5]])}" + ("..." if len(data.members) > 5 else ""),
            
            # Clear unused location fields (places 2-8)
            "place2[0]": "",
            "place3[0]": "",
            "place4[0]": "",
            "place5[0]": "",
            "place6[0]": "",
            "place7[0]": "",
            "place8[0]": "",
            "totalnumber2[0]": "",
            "totalnumber3[0]": "",
            "totalnumber4[0]": "",
            "totalnumber5[0]": "",
            "totalnumber6[0]": "",
            "totalnumber7[0]": "",
            "totalnumber8[0]": "",
            
            # Additional empty fields
            "AWB[0]": "",
            "SED[0]": "",
            "agentsignature[0]": "",
            "sign[0]": "",
            "P1[0]": "",
            "F[0]": ""
        }
        
        # Try PyPDF2 first
        if fill_form(input_pdf_path, output_pdf_path, field_mapping):
            return True
        
        # Fallback to the generic PDF population function from docs.py
        try:
            from .docs import populate_pdf_with_fields
            return populate_pdf_with_fields(input_pdf_path, output_pdf_path, field_mapping)
        except ImportError:
            print("Could not import populate_pdf_with_fields from docs.py")
            return False
        
    except Exception as e:
        print(f"Error populating gen_dec PDF: {e}")
        return False


def create_gen_dec_data_from_trip(trip) -> GenDecData:
    """
    Create GenDecData from a Trip model instance with proper member titles
    
    Args:
        trip: Trip model instance
        
    Returns:
        GenDecData: Populated data structure
    """
    members = []
    
    # Add passengers as PAX
    for passenger in trip.passengers.all():
        if passenger.info:
            name = f"{passenger.info.first_name} {passenger.info.last_name}".strip()
            if name:
                members.append(GenDecMember(
                    name=name, 
                    title="PAX",
                    nationality=passenger.nationality or "",
                    passport_num=passenger.passport_number or ""
                ))
    
    # Add patient as PAX if exists and not already counted
    if trip.patient and trip.patient.info:
        patient_name = f"{trip.patient.info.first_name} {trip.patient.info.last_name}".strip()
        # Check if patient is already in passengers list
        existing_names = [m.name for m in members]
        if patient_name and patient_name not in existing_names:
            members.append(GenDecMember(
                name=patient_name, 
                title="PAX",
                nationality=trip.patient.nationality or "",
                passport_num=trip.patient.passport_number or ""
            ))
    
    # Add crew members from trip lines with proper titles
    crew_added = set()  # Track to avoid duplicates
    for trip_line in trip.trip_lines.all():
        if trip_line.crew_line:
            # Add PIC
            if trip_line.crew_line.primary_in_command:
                pic_name = f"{trip_line.crew_line.primary_in_command.first_name} {trip_line.crew_line.primary_in_command.last_name}".strip()
                if pic_name and pic_name not in crew_added:
                    members.append(GenDecMember(name=pic_name, title="PIC"))
                    crew_added.add(pic_name)
            
            # Add SIC
            if trip_line.crew_line.secondary_in_command:
                sic_name = f"{trip_line.crew_line.secondary_in_command.first_name} {trip_line.crew_line.secondary_in_command.last_name}".strip()
                if sic_name and sic_name not in crew_added:
                    members.append(GenDecMember(name=sic_name, title="SIC"))
                    crew_added.add(sic_name)
            
            # Add medical crew as MED
            for medic in trip_line.crew_line.medic_ids.all():
                medic_name = f"{medic.first_name} {medic.last_name}".strip()
                if medic_name and medic_name not in crew_added:
                    members.append(GenDecMember(name=medic_name, title="MED"))
                    crew_added.add(medic_name)
    
    # Get flight information
    aircraft = trip.aircraft
    first_trip_line = trip.trip_lines.first()
    
    # Create airport objects
    depart_airport = Airport(
        icao=first_trip_line.origin_airport.ident if first_trip_line and first_trip_line.origin_airport else "",
        city=first_trip_line.origin_airport.municipality if first_trip_line and first_trip_line.origin_airport else "",
        country=first_trip_line.origin_airport.iso_country if first_trip_line and first_trip_line.origin_airport else ""
    )
    
    arrive_airport = Airport(
        icao=first_trip_line.destination_airport.ident if first_trip_line and first_trip_line.destination_airport else "",
        city=first_trip_line.destination_airport.municipality if first_trip_line and first_trip_line.destination_airport else "",
        country=first_trip_line.destination_airport.iso_country if first_trip_line and first_trip_line.destination_airport else ""
    )
    
    flight_date = ""
    if first_trip_line and first_trip_line.departure_time_local:
        flight_date = first_trip_line.departure_time_local.strftime('%Y-%m-%d')
    
    return GenDecData(
        owner=aircraft.company if aircraft else 'JET Aviation Operations',
        tail_num=aircraft.tail_number if aircraft else '',
        flight_no=trip.trip_number or '',
        date=flight_date,
        depart=depart_airport,
        arrive=arrive_airport,
        members=members
    )


# Legacy function for backward compatibility
def fill_gen_dec(gen_dec: GenDecData, output_path: str):
    """Legacy function - use populate_gen_dec_pdf_enhanced instead"""
    template_path = "/home/ropolly/projects/work/jetmain/Operations/backend/documents/templates/nosign_pdf/gen_dec.pdf"
    return populate_gen_dec_pdf_enhanced(template_path, output_path, gen_dec)


