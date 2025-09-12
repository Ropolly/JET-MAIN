#!/usr/bin/env python
"""
Debug script to inspect PDF form fields and test field population.
This will help identify why PDFs are coming out empty.
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path
sys.path.append(str(Path(__file__).parent))

def inspect_pdf_fields(pdf_path):
    """Inspect the form fields in a PDF to see what field names exist."""
    print(f"Inspecting PDF fields in: {pdf_path}")
    
    try:
        from pdfrw import PdfReader
        
        reader = PdfReader(pdf_path)
        print(f"PDF has {len(reader.pages)} pages")
        
        field_names = []
        for page_num, page in enumerate(reader.pages):
            print(f"\nPage {page_num + 1}:")
            if page.Annots:
                print(f"  Found {len(page.Annots)} annotations")
                for i, annotation in enumerate(page.Annots):
                    if annotation.T:  # Field name
                        field_name = annotation.T[1:-1]  # Remove parentheses
                        field_names.append(field_name)
                        print(f"    Field {i+1}: '{field_name}'")
                        
                        # Check if it has a value
                        if hasattr(annotation, 'V') and annotation.V:
                            print(f"      Current value: {annotation.V}")
                        else:
                            print(f"      Current value: (empty)")
            else:
                print("  No annotations found")
        
        return field_names
        
    except Exception as e:
        print(f"pdfrw inspection failed: {e}")
        
        # Try with pypdf
        try:
            from pypdf import PdfReader
            
            reader = PdfReader(pdf_path)
            print(f"PDF has {len(reader.pages)} pages")
            
            field_names = []
            if reader.get_form_text_fields():
                fields = reader.get_form_text_fields()
                print(f"Found {len(fields)} form fields:")
                for field_name, value in fields.items():
                    field_names.append(field_name)
                    print(f"  '{field_name}': '{value}'")
            else:
                print("No form fields found with pypdf")
            
            return field_names
            
        except Exception as e2:
            print(f"pypdf inspection also failed: {e2}")
            return []


def test_field_population():
    """Test populating a PDF with known field names."""
    print("\n" + "="*60)
    print("TESTING FIELD POPULATION")
    print("="*60)
    
    try:
        from documents.templates.docs import populate_pdf_with_fields
        
        # Test with Quote PDF
        template_path = 'documents/templates/nosign_pdf/Quote.pdf'
        output_path = 'documents/templates/nosign_out/debug_quote.pdf'
        
        if not Path(template_path).exists():
            print(f"Template not found: {template_path}")
            return False
        
        # Get actual field names from the PDF
        field_names = inspect_pdf_fields(template_path)
        
        if not field_names:
            print("No fields found - PDF might not have form fields")
            return False
        
        # Create test mapping using actual field names
        test_mapping = {}
        for field_name in field_names[:5]:  # Test first 5 fields
            test_mapping[field_name] = f"TEST_VALUE_{field_name}"
        
        print(f"\nTesting with mapping: {test_mapping}")
        
        # Ensure output directory exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Try to populate
        result = populate_pdf_with_fields(template_path, output_path, test_mapping)
        
        if result:
            print(f"✓ PDF populated successfully: {output_path}")
            
            # Verify the output has the values
            output_fields = inspect_pdf_fields(output_path)
            print(f"\nVerifying output PDF...")
            return True
        else:
            print("✗ PDF population failed")
            return False
            
    except Exception as e:
        print(f"Test failed: {e}")
        return False


def main():
    """Main debug function."""
    print("PDF FIELD DEBUG TOOL")
    print("="*60)
    
    # Check all template PDFs
    templates = [
        'documents/templates/nosign_pdf/Quote.pdf',
        'documents/templates/nosign_pdf/itin.pdf',
        'documents/templates/nosign_pdf/handling_request.pdf'
    ]
    
    for template in templates:
        if Path(template).exists():
            print(f"\n{'='*60}")
            print(f"ANALYZING: {template}")
            print(f"{'='*60}")
            inspect_pdf_fields(template)
        else:
            print(f"\n✗ Template not found: {template}")
    
    # Test field population
    test_field_population()


if __name__ == '__main__':
    main()
