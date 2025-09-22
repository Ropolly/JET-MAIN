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
class GeneralDeclarationData:
    """Data class for General Declaration PDF fields - matches actual PDF field names"""
    # Aircraft information
    marks_of_nationality: str = ''  # Aircraft registration/tail number
    owner_or_operator: str = ''     # Company/operator name
    
    # Flight information
    flight_number: str = ''
    departure_from: str = ''        # Origin airport
    arrival_at: str = ''           # Destination airport
    date: str = ''                 # Flight date
    
    # Passenger/crew counts for different locations (up to 8 places)
    place1: str = ''               # Location name
    place2: str = ''
    place3: str = ''
    place4: str = ''
    place5: str = ''
    place6: str = ''
    place7: str = ''
    place8: str = ''
    
    # Total numbers for each place
    total_number1: str = ''        # Total passengers/crew at place1
    total_number2: str = ''
    total_number3: str = ''
    total_number4: str = ''
    total_number5: str = ''
    total_number6: str = ''
    total_number7: str = ''
    total_number8: str = ''
    
    # Passenger movement
    embarking: str = ''            # Number embarking
    disembarking: str = ''         # Number disembarking
    through_on_same_flight: str = '' # Through passengers
    through_on_same_flight2: str = '' # Additional through passengers
    
    # Additional fields
    awb: str = ''                  # Air Waybill number
    sed: str = ''                  # Shipper's Export Declaration
    declaration1: str = ''         # Declaration text
    details1: str = ''            # Additional details
    other1: str = ''              # Other information
    
    # Signatures
    agent_signature: str = ''      # Agent signature
    sign: str = ''                # Additional signature field


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


def populate_pdf_with_fields(input_pdf_path: str, output_pdf_path: str, field_mapping: dict) -> bool:
    """
    Generic function to populate PDF form fields with data
    
    Args:
        input_pdf_path: Path to the template PDF
        output_pdf_path: Path where the filled PDF will be saved
        field_mapping: Dictionary mapping field names to values
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Try PyMuPDF (fitz) method first - most reliable for form filling
        import fitz
        
        doc = fitz.open(input_pdf_path)
        
        # Clean field mapping - ensure all values are strings
        clean_mapping = {}
        for field_name, value in field_mapping.items():
            if value is not None:
                clean_mapping[field_name] = str(value)
            else:
                clean_mapping[field_name] = ""
        
        # Fill form fields
        for page_num in range(len(doc)):
            page = doc[page_num]
            widgets = page.widgets()
            
            for widget in widgets:
                if widget.field_name in clean_mapping:
                    widget.field_value = clean_mapping[widget.field_name]
                    widget.update()
        
        # Save the filled PDF
        doc.save(output_pdf_path)
        doc.close()
        return True
        
    except Exception as e:
        print(f"PyMuPDF failed: {e}")
        
        # Fallback to pdfrw method
        try:
            from pdfrw import PdfReader, PdfWriter, PdfDict
            
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
                                annotation.update(PdfDict(V=f'({clean_mapping[field_name]})'))
                                annotation.update(PdfDict(DV=f'({clean_mapping[field_name]})'))
            
            # Write the filled PDF
            PdfWriter(output_pdf_path, trailer=template_pdf).write()
            return True
            
        except Exception as e2:
            print(f"All PDF population methods failed: {e2}")
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
    # Note: depart/arrive fields should contain TIMES not ICAO codes
    field_mapping = {
        'company': data.company,
        'make': data.make,
        'model': data.model,
        'tail_number': data.tail_number,
        'serial_number': data.serial_number,
        'mgtow': data.mgtow,
        'mission': data.mission,
        'depart_origin': data.depart_origin,  # Should be departure TIME from origin
        'arrive_dest': data.arrive_dest,      # Should be arrival TIME at destination
        'depart_dest': data.depart_dest,      # Should be departure TIME from destination (return leg)
        'arrive_origin': data.arrive_origin   # Should be arrival TIME back at origin (return leg)
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
    """Populate itin-2.pdf with data from ItineraryData instance"""
    # Map data to actual PDF field names from itin-2.pdf
    # NOTE: Now includes header fields that were missing in the old itin.pdf template
    field_mapping = {
        'trip_number': data.trip_number,
        'trip_date': data.trip_date,
        'trip_type': data.trip_type,
        'tail_number': data.tail_number,
        'patient_name': data.patient_name,
        'bed_at_origin': 'Yes' if data.bed_at_origin else 'No',
        'bed_at_dest': 'Yes' if data.bed_at_dest else 'No',
        'special_instructions': data.special_instructions,
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


def populate_gen_dec_pdf(input_pdf_path: str, output_pdf_path: str, data: GeneralDeclarationData) -> bool:
    """Populate gen_dec.pdf with data from GeneralDeclarationData instance"""
    # Map data to actual PDF field names from gen_dec.pdf
    field_mapping = {
        # Aircraft information
        'MarksofNationality[0]': data.marks_of_nationality,
        'OwnerorOperator[0]': data.owner_or_operator,
        
        # Flight information
        'flightnumber[0]': data.flight_number,
        'departurefrom[0]': data.departure_from,
        'arrivaat[0]': data.arrival_at,
        'Date[0]': data.date,
        
        # Places and totals (up to 8 locations)
        'place1[0]': data.place1,
        'place2[0]': data.place2,
        'place3[0]': data.place3,
        'place4[0]': data.place4,
        'place5[0]': data.place5,
        'place6[0]': data.place6,
        'place7[0]': data.place7,
        'place8[0]': data.place8,
        
        'totalnumber1[0]': data.total_number1,
        'totalnumber2[0]': data.total_number2,
        'totalnumber3[0]': data.total_number3,
        'totalnumber4[0]': data.total_number4,
        'totalnumber5[0]': data.total_number5,
        'totalnumber6[0]': data.total_number6,
        'totalnumber7[0]': data.total_number7,
        'totalnumber8[0]': data.total_number8,
        
        # Passenger movement
        'embarking[0]': data.embarking,
        'disembarking[0]': data.disembarking,
        'throughonsameflight[0]': data.through_on_same_flight,
        'throughonsameflight2[0]': data.through_on_same_flight2,
        
        # Additional fields
        'AWB[0]': data.awb,
        'SED[0]': data.sed,
        'declaration1[0]': data.declaration1,
        'details1[0]': data.details1,
        'other1[0]': data.other1,
        
        # Signatures
        'agentsignature[0]': data.agent_signature,
        'sign[0]': data.sign,
        
        # Additional fields found
        'P1[0]': '',  # Empty for now
        'F[0]': ''    # Empty for now
    }
    
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

