#!/usr/bin/env python3

try:
    import PyPDF2
    from PyPDF2 import PdfReader
    PYPDF2_AVAILABLE = True
except ImportError:
    PYPDF2_AVAILABLE = False

try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False

from pathlib import Path
import sys

def inspect_pdf_with_pypdf2(pdf_path):

    print(" INSPECTING WITH PYPDF2")
    print("-" * 40)
    
    try:
        with open(pdf_path, 'rb') as file:
            reader = PdfReader(file)
            
            print(f" Pages: {len(reader.pages)}")
            print(f" Is encrypted: {reader.is_encrypted}")
            
            # Check for form fields
            if "/AcroForm" in reader.trailer["/Root"]:
                print(" PDF contains form fields (AcroForm)")
                
                form = reader.trailer["/Root"]["/AcroForm"]
                if "/Fields" in form:
                    fields = form["/Fields"]
                    print(f" Form fields found: {len(fields)}")
                    
                    # Extract field information
                    for i, field_ref in enumerate(fields):
                        try:
                            field = field_ref.get_object()
                            field_name = field.get("/T", "Unknown")
                            field_type = field.get("/FT", "Unknown")
                            field_value = field.get("/V", "")
                            
                            print(f"   Field {i+1}: {field_name} (Type: {field_type}, Value: '{field_value}')")
                        except Exception as e:
                            print(f"   Field {i+1}: Error reading - {str(e)}")
                else:
                    print(" No fields array found in AcroForm")
            else:
                print(" No AcroForm found - may not be a fillable PDF")
                
        return True
        
    except Exception as e:
        print(f" PyPDF2 inspection failed: {str(e)}")
        return False

def inspect_pdf_with_pymupdf(pdf_path):

    print("\n INSPECTING WITH PYMUPDF")
    print("-" * 40)
    
    try:
        doc = fitz.open(pdf_path)
        print(f" Pages: {doc.page_count}")
        print(f" Is PDF: {doc.is_pdf}")
        print(f" Is encrypted: {doc.needs_pass}")
        
        total_fields = 0
        for page_num in range(doc.page_count):
            page = doc[page_num]
            widgets = page.widgets()
            
            if widgets:
                print(f"\n Page {page_num + 1} form fields:")
                for widget in widgets:
                    total_fields += 1
                    field_name = widget.field_name or "Unnamed"
                    field_type = widget.field_type_string
                    field_value = widget.field_value or ""
                    
                    print(f"   {field_name} (Type: {field_type}, Value: '{field_value}')")
            else:
                print(f"\n Page {page_num + 1}: No form fields found")
        
        print(f"\n Total form fields: {total_fields}")
        doc.close()
        return True
        
    except Exception as e:
        print(f" PyMuPDF inspection failed: {str(e)}")
        return False

def inspect_pdf_basic_info(pdf_path):

    print(" BASIC PDF INSPECTION")
    print("-" * 40)
    
    try:
        file_size = pdf_path.stat().st_size
        print(f" File size: {file_size:,} bytes")
        
        # Read first few KB to look for PDF structure
        with open(pdf_path, 'rb') as f:
            header = f.read(1024).decode('latin-1', errors='ignore')
            
        if '%PDF' in header:
            print(" Valid PDF file detected")
            
            # Look for form-related keywords
            form_keywords = ['/AcroForm', '/Fields', '/FT', '/Tx', '/Ch']
            found_keywords = [kw for kw in form_keywords if kw in header]
            
            if found_keywords:
                print(f" Form indicators found: {', '.join(found_keywords)}")
            else:
                print("  No form indicators in header (may be deeper in file)")
        else:
            print(" Invalid PDF format")
        
        return True
        
    except Exception as e:
        print(f" Basic inspection failed: {str(e)}")
        return False

def main():

    print(" PDF FORM FIELD INSPECTION")
    print("=" * 60)
    
    pdf_path = Path(__file__).parent / "documents" / "GenDec.pdf"
    
    if not pdf_path.exists():
        print(f" PDF file not found: {pdf_path}")
        return False
    
    print(f" Inspecting: {pdf_path.name}")
    print(f" Full path: {pdf_path}")
    
    # Check available libraries
    print(f"\n Available libraries:")
    print(f"   PyPDF2: {'' if PYPDF2_AVAILABLE else ''}")
    print(f"   PyMuPDF: {'' if PYMUPDF_AVAILABLE else ''}")
    
    # Run inspections
    success = False
    
    # Basic inspection always works
    if inspect_pdf_basic_info(pdf_path):
        success = True
    
    # Try PyPDF2 if available
    if PYPDF2_AVAILABLE:
        if inspect_pdf_with_pypdf2(pdf_path):
            success = True
    
    # Try PyMuPDF if available
    if PYMUPDF_AVAILABLE:
        if inspect_pdf_with_pymupdf(pdf_path):
            success = True
    
    # Installation suggestions if no libraries available
    if not PYPDF2_AVAILABLE and not PYMUPDF_AVAILABLE:
        print("\n INSTALLATION SUGGESTIONS:")
        print("   pip install PyPDF2")
        print("   pip install PyMuPDF")
    
    return success

if __name__ == "__main__":
    success = main()
    print(f"\n{' INSPECTION COMPLETE' if success else ' INSPECTION FAILED'}")
    sys.exit(0 if success else 1)
