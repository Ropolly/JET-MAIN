#!/usr/bin/env python
"""
Debug script to find the exact field names for trip_number, trip_date, trip_type, tail_number in itinerary PDF.
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path
sys.path.append(str(Path(__file__).parent))

def find_missing_fields():
    """Find the exact field names for the missing fields in itinerary PDF."""
    print("Searching for trip_number, trip_date, trip_type, tail_number fields in itinerary PDF...")
    
    try:
        from pdfrw import PdfReader
        
        template_path = 'documents/templates/nosign_pdf/itin.pdf'
        reader = PdfReader(template_path)
        
        all_fields = []
        for page_num, page in enumerate(reader.pages):
            print(f"\nPage {page_num + 1}:")
            if page.Annots:
                for i, annotation in enumerate(page.Annots):
                    if annotation.T:  # Field name
                        field_name = annotation.T[1:-1]  # Remove parentheses
                        all_fields.append(field_name)
                        
                        # Look for fields that might be our missing ones
                        field_lower = field_name.lower()
                        if any(keyword in field_lower for keyword in ['trip', 'tail', 'date', 'type', 'number']):
                            print(f"    POTENTIAL MATCH: '{field_name}'")
        
        print(f"\n{'='*60}")
        print("ALL FIELD NAMES IN ITINERARY PDF:")
        print(f"{'='*60}")
        
        for i, field in enumerate(all_fields, 1):
            print(f"{i:3d}. '{field}'")
        
        print(f"\n{'='*60}")
        print("SEARCHING FOR SPECIFIC PATTERNS:")
        print(f"{'='*60}")
        
        # Search for specific patterns
        patterns = {
            'trip_number': ['trip', 'number', 'trip_number', 'tripnumber'],
            'trip_date': ['date', 'trip_date', 'tripdate'],
            'trip_type': ['type', 'trip_type', 'triptype'],
            'tail_number': ['tail', 'tail_number', 'tailnumber', 'aircraft']
        }
        
        for missing_field, search_terms in patterns.items():
            print(f"\nLooking for {missing_field}:")
            matches = []
            for field in all_fields:
                field_lower = field.lower()
                for term in search_terms:
                    if term in field_lower:
                        matches.append(field)
                        break
            
            if matches:
                print(f"  Possible matches: {matches}")
            else:
                print(f"  No matches found")
        
        return all_fields
        
    except Exception as e:
        print(f"Error: {e}")
        return []


def test_field_mapping():
    """Test if our current field mapping includes the basic fields."""
    print(f"\n{'='*60}")
    print("CHECKING CURRENT FIELD MAPPING:")
    print(f"{'='*60}")
    
    try:
        from documents.templates.docs import ItineraryData, populate_itinerary_pdf
        
        # Check what fields we're currently mapping
        template_path = 'documents/templates/nosign_pdf/itin.pdf'
        output_path = 'documents/templates/nosign_out/debug_itinerary_mapping.pdf'
        
        # Create minimal test data
        test_data = ItineraryData(
            trip_number='TEST-TRIP-123',
            tail_number='N123TEST',
            trip_date='2025-01-20',
            trip_type='Medical Test'
        )
        
        # Ensure output directory exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Try to populate
        result = populate_itinerary_pdf(template_path, output_path, test_data)
        
        if result:
            print("✓ PDF generation successful")
            
            # Check what got populated
            from debug_pdf_fields import inspect_pdf_fields
            print("\nChecking populated fields:")
            inspect_pdf_fields(output_path)
        else:
            print("✗ PDF generation failed")
            
    except Exception as e:
        print(f"Error testing field mapping: {e}")


def main():
    """Main debug function."""
    print("DEBUGGING MISSING ITINERARY FIELDS")
    print("=" * 60)
    
    find_missing_fields()
    test_field_mapping()


if __name__ == '__main__':
    main()
