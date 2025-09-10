import pypdf
from pypdf import PdfWriter, PdfReader
import PyPDF2
from typing import Dict, Any, Optional, List
from datetime import datetime
from dataclasses import dataclass, field


# Data Classes for PDF Population

@dataclass
class QuoteData:
    """Data class for Quote PDF fields - matches actual PDF field names"""
    quote_id: str = ''
    inquiry_date: str = ''
    patient_name: str = ''
    aircraft_type: str = ''
    pickup_airport: str = ''
    dropoff_airport: str = ''
    trip_date: str = ''
    esitmated_flight_time: str = ''
    number_of_stops: str = ''
    medical_team: str = ''
    include_grounds: str = ''
    our_availability: str = ''
    amount: str = ''
    notes: str = ''


@dataclass
class PassengerInfo:
    """Passenger information for handling requests"""
    name: str = ""
    title: str = ""
    nationality: str = ""
    date_of_birth: str = ""
    passport_number: str = ""
    passport_expiration: str = ""
    contact_number: str = ""


@dataclass
class HandlingRequestData:
    """Data class for Handling Request PDF fields - matches actual PDF field names"""
    company: str = ''
    make: str = ''
    model: str = ''
    tail_number: str = ''
    serial_number: str = ''
    mgtow: str = ''
    mission: str = ''
    depart_origin: str = ''
    arrive_dest: str = ''
    depart_dest: str = ''
    arrive_origin: str = ''
    passengers: List[PassengerInfo] = field(default_factory=list)


@dataclass
class CrewInfo:
    """Crew information for itinerary"""
    pic: str = ""  # Pilot in Command
    sic: str = ""  # Second in Command
    med_1: str = ""  # Medical crew member 1
    med_2: str = ""  # Medical crew member 2
    med_4: str = ""  # Medical crew member 4


@dataclass
class FlightLeg:
    """Flight leg information"""
    leg: str = ""
    departure_id: str = ""
    edt_utc_local: str = ""
    arrival_id: str = ""
    flight_time: str = ""
    eta_utc_local: str = ""
    ground_time: str = ""
    pax_leg: str = ""


@dataclass
class AirportInfo:
    """Airport information"""
    icao: str = ""
    airport_city_name: str = ""
    state_country: str = ""
    time_zone: str = ""
    fbo_handler: str = ""
    freq: str = ""
    phone_fax: str = ""
    fuel: str = ""


@dataclass
class TimeInfo:
    """Time information for itinerary"""
    showtime: str = ""
    origin_edt: str = ""
    total_flight_time: str = ""
    total_duty_time: str = ""
    pre_flight_duty_time: str = ""
    post_flight_duty_time: str = ""


@dataclass
class ItineraryData:
    """Data class for Itinerary PDF fields"""
    trip_number: str = ""
    tail_number: str = ""
    trip_date: str = ""
    trip_type: str = ""
    patient_name: str = ""
    bed_at_origin: bool = False  # Boolean field - will be converted to Yes/No
    bed_at_dest: bool = False    # Boolean field - will be converted to Yes/No
    special_instructions: str = ""
    passengers: List[str] = field(default_factory=list)  # List of passenger names
    crew: CrewInfo = field(default_factory=CrewInfo)
    flight_legs: List[FlightLeg] = field(default_factory=list)
    airports: List[AirportInfo] = field(default_factory=list)
    times: TimeInfo = field(default_factory=TimeInfo)
    apis: str = ""
    apis_2: str = ""
    gen_dec: str = ""
    gen_dec_2: str = ""


def populate_pdf_with_fields(input_pdf_path: str, output_pdf_path: str, field_mapping: Dict[str, str]) -> bool:
    """
    Generic function to populate PDF form fields using pdfrw.
    
    Args:
        input_pdf_path: Path to the input PDF template
        output_pdf_path: Path where the filled PDF will be saved
        field_mapping: Dictionary mapping field names to values
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        from pdfrw import PdfReader, PdfWriter, PdfDict, PdfName
        
        # Read the PDF
        template_pdf = PdfReader(input_pdf_path)
        
        # Clean field mapping - ensure all values are strings
        clean_mapping = {}
        for field_name, value in field_mapping.items():
            if value is not None:
                clean_mapping[field_name] = str(value)
            else:
                clean_mapping[field_name] = ""
        
        # Find and populate form fields
        for page in template_pdf.pages:
            if page.Annots:
                for annotation in page.Annots:
                    if annotation.T:  # Field name
                        field_name = annotation.T[1:-1]  # Remove parentheses
                        if field_name in clean_mapping:
                            # Set the field value
                            annotation.update(PdfDict(V=clean_mapping[field_name]))
                            # Also set appearance value
                            annotation.update(PdfDict(AP=''))
        
        # Write the filled PDF
        PdfWriter(output_pdf_path, trailer=template_pdf).write()
        return True
        
    except Exception as e:
        print(f"pdfrw failed: {e}")
        # Fallback to pypdf
        try:
            from pypdf import PdfReader, PdfWriter
            
            reader = PdfReader(input_pdf_path)
            writer = PdfWriter()
            
            # Copy pages
            for page in reader.pages:
                writer.add_page(page)
            
            # Clean field mapping
            clean_mapping = {}
            for field_name, value in field_mapping.items():
                if value is not None:
                    clean_mapping[field_name] = str(value)
                else:
                    clean_mapping[field_name] = ""
            
            # Update form fields
            writer.update_page_form_field_values(writer.pages[0], clean_mapping)
            
            # Write output
            with open(output_pdf_path, 'wb') as output_file:
                writer.write(output_file)
                
            return True
            
        except Exception as e2:
            print(f"All methods failed: {e2}")
            return False


def populate_quote_pdf(input_pdf_path: str, output_pdf_path: str, data: QuoteData) -> bool:
    """Populate Quote.pdf with data from QuoteData instance"""
    # Map data to actual PDF field names from Quote.pdf
    field_mapping = {
        'quote_id': data.quote_id,
        'inquiry_date': data.inquiry_date,
        'patient_name': data.patient_name,
        'aircraft_type': data.aircraft_type,
        'pickup_airport': data.pickup_airport,
        'dropoff_airport': data.dropoff_airport,
        'trip_date': data.trip_date,
        'esitmated_flight_time': data.esitmated_flight_time,
        'number_of_stops': data.number_of_stops,
        'medical_team': data.medical_team,
        'include_grounds': data.include_grounds,
        'our_availability': data.our_availability,
        'amount': data.amount,
        'notes': data.notes
    }
    
    return populate_pdf_with_fields(input_pdf_path, output_pdf_path, field_mapping)


def populate_handling_request_pdf(input_pdf_path: str, output_pdf_path: str, data: HandlingRequestData) -> bool:
    """Populate handling_request.pdf with data from HandlingRequestData instance"""
    # Map data to actual PDF field names from handling_request.pdf
    field_mapping = {
        'company': data.company,
        'make': data.make,
        'model': data.model,
        'tail_number': data.tail_number,
        'serial_number': data.serial_number,
        'mgtow': data.mgtow,
        'mission': data.mission,
        'depart_origin': data.depart_origin,
        'arrive_dest': data.arrive_dest,
        'depart_dest': data.depart_dest,
        'arrive_origin': data.arrive_origin
    }
    
    # Add passenger information (up to 8 passengers)
    for i in range(1, 9):
        if i <= len(data.passengers):
            passenger = data.passengers[i-1]
            field_mapping.update({
                f'r{i}_name': passenger.name,
                f'r{i}_title': passenger.title,
                f'r{i}_nationality': passenger.nationality,
                f'r{i}_date_of_birth': passenger.date_of_birth,
                f'r{i}_passport_number': passenger.passport_number,
                f'r{i}_passport_expiration': passenger.passport_expiration,
                f'r{i}_contact_number': passenger.contact_number
            })
        else:
            # Fill empty fields for unused passenger slots
            field_mapping.update({
                f'r{i}_name': '',
                f'r{i}_title': '',
                f'r{i}_nationality': '',
                f'r{i}_date_of_birth': '',
                f'r{i}_passport_number': '',
                f'r{i}_passport_expiration': '',
                f'r{i}_contact_number': ''
            })
    
    return populate_pdf_with_fields(input_pdf_path, output_pdf_path, field_mapping)


def populate_itinerary_pdf(input_pdf_path: str, output_pdf_path: str, data: ItineraryData) -> bool:
    """
    Populate the itin.pdf (itinerary) with provided data using actual PDF field names.
    
    Args:
        input_pdf_path: Path to the input PDF template
        output_pdf_path: Path where the filled PDF will be saved
        data: ItineraryData instance containing all the data to populate
        
    Returns:
        bool: True if successful, False otherwise
    """
    # Map basic itinerary data to actual PDF field names
    field_mapping = {
        'trip_number': data.trip_number,
        'tail_number': data.tail_number,
        'trip_date': data.trip_date,
        'trip_type': data.trip_type,
        'patient_name': data.patient_name,
        'bed_at_origin': 'Yes' if data.bed_at_origin else 'No',
        'bed_at_dest': 'Yes' if data.bed_at_dest else 'No',
        'special_instructions': data.special_instructions
    }
    
    # Add passenger information (up to 5 passengers)
    for i in range(1, 6):
        if i <= len(data.passengers):
            field_mapping[f'pax_{i}'] = data.passengers[i-1]
        else:
            field_mapping[f'pax_{i}'] = ''
    
    # Add crew information
    field_mapping.update({
        'pic': data.crew.pic,
        'sic': data.crew.sic,
        'med_1': data.crew.med_1,
        'med_2': data.crew.med_2
    })
    
    # Add flight legs (up to 10 legs)
    for i in range(1, 11):
        if i <= len(data.flight_legs):
            leg = data.flight_legs[i-1]
            field_mapping.update({
                f'LegRow{i}': leg.leg,
                f'Departure IDRow{i}': leg.departure_id,
                f'EDT UTCLOCALRow{i}': leg.edt_utc_local,
                f'Arrival IDRow{i}': leg.arrival_id,
                f'Flight TimeRow{i}': leg.flight_time,
                f'ETA UTCLOCALRow{i}': leg.eta_utc_local,
                f'Ground TimeRow{i}': leg.ground_time,
                f'PAX LegRow{i}': leg.pax_leg
            })
        else:
            # Fill empty fields for unused leg slots
            field_mapping.update({
                f'LegRow{i}': '',
                f'Departure IDRow{i}': '',
                f'EDT UTCLOCALRow{i}': '',
                f'Arrival IDRow{i}': '',
                f'Flight TimeRow{i}': '',
                f'ETA UTCLOCALRow{i}': '',
                f'Ground TimeRow{i}': '',
                f'PAX LegRow{i}': ''
            })
    
    # Add airport information (up to 11 airports)
    for i in range(1, 12):
        if i <= len(data.airports):
            airport = data.airports[i-1]
            field_mapping.update({
                f'ICAORow{i}': airport.icao,
                f'Airport City NameRow{i}': airport.airport_city_name,
                f'State CountryRow{i}': airport.state_country,
                f'Time ZoneRow{i}': airport.time_zone,
                f'FBOHandlerRow{i}': airport.fbo_handler,
                f'FreqRow{i}': airport.freq,
                f'Phone FaxRow{i}': airport.phone_fax,
                f'Fuel  Row{i}': airport.fuel  # Note the extra space in "Fuel  Row"
            })
        else:
            # Fill empty fields for unused airport slots
            field_mapping.update({
                f'ICAORow{i}': '',
                f'Airport City NameRow{i}': '',
                f'State CountryRow{i}': '',
                f'Time ZoneRow{i}': '',
                f'FBOHandlerRow{i}': '',
                f'FreqRow{i}': '',
                f'Phone FaxRow{i}': '',
                f'Fuel  Row{i}': ''  # Note the extra space in "Fuel  Row"
            })
    
    # Add timing information
    field_mapping.update({
        'showtime': data.times.showtime,
        'origin_edt': data.times.origin_edt,
        'total_filght_time': data.times.total_flight_time,  # Note: PDF has typo "filght"
        'total_duty_time': data.times.total_duty_time,
        'pre_flight_duty_time': data.times.pre_flight_duty_time,
        'post_flight_duty_time': data.times.post_flight_duty_time
    })
        
    return populate_pdf_with_fields(input_pdf_path, output_pdf_path, field_mapping)


# Example usage functions
def example_populate_quote():
    """Example of how to use the populate_quote_pdf function"""
    sample_data = QuoteData(
        quote_id='Q-2024-001',
        inquiry_date='2024-01-15',
        patient_name='John Smith',
        aircraft_type='Citation CJ3',
        pickup_airport='KJFK',
        dropoff_airport='KLAX',
        trip_date='2024-02-01',
        esitmated_flight_time='5:30',
        number_of_stops='0',
        medical_team='Dr. Johnson, Nurse Williams',
        include_grounds='Yes',
        our_availability='Available',
        amount='$24,255',
        notes='Medical transport with specialized equipment'
    )
    
    return populate_quote_pdf('Quote.pdf', 'Quote_filled.pdf', sample_data)

