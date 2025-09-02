#!/usr/bin/env python3

import fitz  # PyMuPDF
from pathlib import Path
from datetime import datetime
import os
import sys

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent.parent.parent
sys.path.append(str(backend_dir))

class GenDecPDFFiller:

    def __init__(self):
        self.documents_dir = Path(__file__).parent / "documents"
        self.outputs_dir = Path(__file__).parent / "pdf_outputs"
        self.outputs_dir.mkdir(parents=True, exist_ok=True)
        
        # Map our data fields to actual PDF form field names
        self.field_mapping = {
            # Basic aircraft and flight info
            'owner_operator': 'F[0].P1[0].OwnerorOperator[0]',
            'aircraft_registration': 'F[0].P1[0].MarksofNationality[0]',
            'flight_number': 'F[0].P1[0].flightnumber[0]',
            'date': 'F[0].P1[0].Date[0]',
            'departure_from': 'F[0].P1[0].departurefrom[0]',
            'arrive_at': 'F[0].P1[0].arrivaat[0]',
            
            # Passenger/crew counts by destination
            'place1': 'F[0].P1[0].place1[0]',
            'place2': 'F[0].P1[0].place2[0]',
            'place3': 'F[0].P1[0].place3[0]',
            'place4': 'F[0].P1[0].place4[0]',
            'place5': 'F[0].P1[0].place5[0]',
            'place6': 'F[0].P1[0].place6[0]',
            'place7': 'F[0].P1[0].place7[0]',
            'place8': 'F[0].P1[0].place8[0]',
            
            # Total numbers for each destination
            'total1': 'F[0].P1[0].totalnumber1[0]',
            'total2': 'F[0].P1[0].totalnumber2[0]',
            'total3': 'F[0].P1[0].totalnumber3[0]',
            'total4': 'F[0].P1[0].totalnumber4[0]',
            'total5': 'F[0].P1[0].totalnumber5[0]',
            'total6': 'F[0].P1[0].totalnumber6[0]',
            'total7': 'F[0].P1[0].totalnumber7[0]',
            'total8': 'F[0].P1[0].totalnumber8[0]',
            
            # Passenger counts
            'embarking': 'F[0].P1[0].embarking[0]',
            'through_passengers': 'F[0].P1[0].throughonsameflight[0]',
            'disembarking': 'F[0].P1[0].disembarking[0]',
            'through_passengers2': 'F[0].P1[0].throughonsameflight2[0]',
            
            # Declarations and other info
            'declaration': 'F[0].P1[0].declaration1[0]',
            'other_info': 'F[0].P1[0].other1[0]',
            'details': 'F[0].P1[0].details1[0]',
            
            # Signature fields (text for now, signature fields need special handling)
            'captain_signature': 'F[0].P1[0].sign[0]',
            'agent_signature': 'F[0].P1[0].agentsignature[0]',
            
            # Reference numbers
            'sed_number': 'F[0].P1[0].SED[0]',
            'awb_number': 'F[0].P1[0].AWB[0]'
        }

    def prepare_flight_data(self, mock_trip_line=None):

        if mock_trip_line:
            # Use provided mock data
            return mock_trip_line
        
        # Create comprehensive mock data for testing
        return {
            # Basic Info
            'owner_operator': 'JET Charter Services LLC',
            'aircraft_registration': 'N123JT',
            'flight_number': 'JET001',
            'date': datetime.now().strftime('%m/%d/%Y'),
            'departure_from': 'Los Angeles International Airport (KLAX)',
            'arrive_at': 'John F. Kennedy International Airport (KJFK)',
            
            # Destinations and passenger counts (simplified for this route)
            'place1': 'New York (KJFK)',
            'total1': '3',  # 2 passengers + 1 patient
            'place2': '',
            'total2': '',
            'place3': '',
            'total3': '',
            'place4': '',
            'total4': '',
            'place5': '',
            'total5': '',
            'place6': '',
            'total6': '',
            'place7': '',
            'total7': '',
            'place8': '',
            'total8': '',
            
            # Passenger movement
            'embarking': '3',  # Total embarking passengers
            'through_passengers': '0',  # Through passengers
            'disembarking': '3',  # Total disembarking
            'through_passengers2': '0',  # Through passengers at destination
            
            # Declarations
            'declaration': 'Medical transport flight - emergency patient transfer',
            'other_info': 'Patient requires continuous medical supervision',
            'details': 'Flight crew: 2, Medical crew: 1, Patient: 1, Accompanying: 1',
            
            # Signatures (text representation)
            'captain_signature': 'Captain John Smith',
            'agent_signature': 'JET Charter Services LLC',
            
            # Reference numbers
            'sed_number': '',
            'awb_number': 'JET001-2024'
        }

    def fill_pdf_form(self, data, output_filename=None):

        template_path = self.documents_dir / "GenDec.pdf"
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")
        
        # Generate output filename
        if not output_filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"GenDec_Filled_{timestamp}.pdf"
        
        output_path = self.outputs_dir / output_filename
        
        print(f" Filling PDF form: {template_path.name}")
        print(f" Output: {output_filename}")
        
        try:
            # Open the PDF
            doc = fitz.open(template_path)
            
            # Track filled fields
            filled_count = 0
            total_fields = 0
            
            # Fill form fields on all pages
            for page_num in range(doc.page_count):
                page = doc[page_num]
                widgets = list(page.widgets())
                
                print(f"\n Processing page {page_num + 1} ({len(widgets)} fields)")
                
                for widget in widgets:
                    total_fields += 1
                    field_name = widget.field_name
                    
                    # Find matching data for this field
                    data_key = None
                    for key, pdf_field in self.field_mapping.items():
                        if pdf_field == field_name:
                            data_key = key
                            break
                    
                    if data_key and data_key in data and data[data_key]:
                        # Fill the field
                        widget.field_value = str(data[data_key])
                        widget.update()
                        filled_count += 1
                        print(f"    {field_name} = '{data[data_key]}'")
                    else:
                        print(f"   ⏭  {field_name} (no data)")
            
            print(f"\n Filled {filled_count}/{total_fields} form fields")
            
            # Save the filled PDF
            doc.save(output_path)
            doc.close()
            
            # Verify output
            output_size = output_path.stat().st_size
            print(f" Filled PDF saved: {output_size:,} bytes")
            
            return {
                'success': True,
                'output_path': output_path,
                'output_size': output_size,
                'fields_filled': filled_count,
                'total_fields': total_fields,
                'completion_rate': (filled_count / total_fields * 100) if total_fields > 0 else 0
            }
            
        except Exception as e:
            print(f" PDF filling failed: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'fields_filled': 0,
                'total_fields': 0
            }

    def test_pdf_filling(self):

        print(" TESTING PDF FORM FILLING")
        print("=" * 60)
        
        # Test with mock data
        test_data = self.prepare_flight_data()
        result = self.fill_pdf_form(test_data, "GenDec_Test_Fill.pdf")
        
        if result['success']:
            print(f"\n PDF FILLING SUCCESS!")
            print(f" Completion rate: {result['completion_rate']:.1f}%")
            print(f" Output file: {result['output_path']}")
            
            # Verify the filled PDF
            self.verify_filled_pdf(result['output_path'])
        else:
            print(f"\n PDF FILLING FAILED: {result['error']}")
        
        return result

    def verify_filled_pdf(self, pdf_path):

        print(f"\n VERIFYING FILLED PDF")
        print("-" * 40)
        
        try:
            doc = fitz.open(pdf_path)
            
            filled_fields = []
            empty_fields = []
            
            for page_num in range(doc.page_count):
                page = doc[page_num]
                widgets = list(page.widgets())
                
                for widget in widgets:
                    field_name = widget.field_name
                    field_value = widget.field_value
                    
                    if field_value:
                        filled_fields.append(f"{field_name}: '{field_value}'")
                    else:
                        empty_fields.append(field_name)
            
            doc.close()
            
            print(f" Filled fields ({len(filled_fields)}):")
            for field in filled_fields[:10]:  # Show first 10
                print(f"   {field}")
            if len(filled_fields) > 10:
                print(f"   ... and {len(filled_fields) - 10} more")
            
            if empty_fields:
                print(f"\n⏭  Empty fields ({len(empty_fields)}):")
                for field in empty_fields[:5]:  # Show first 5
                    print(f"   {field}")
                if len(empty_fields) > 5:
                    print(f"   ... and {len(empty_fields) - 5} more")
            
            return len(filled_fields), len(empty_fields)
            
        except Exception as e:
            print(f" Verification failed: {str(e)}")
            return 0, 0

def main():

    filler = GenDecPDFFiller()
    result = filler.test_pdf_filling()
    
    return result['success']

if __name__ == "__main__":
    success = main()
    print(f"\n{' TEST COMPLETED SUCCESSFULLY' if success else ' TEST FAILED'}")
    sys.exit(0 if success else 1)
