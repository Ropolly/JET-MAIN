"""
Document Generation API Views

This module provides API endpoints for generating aviation documents
such as General Declaration (GenDec) and Handling Request documents.
"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from .models import TripLine
from utils.docgen.docgen import DocumentGenerator


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generate_gendec(request, trip_line_id):
    """
    Generate General Declaration (GenDec) document for a trip line.
    
    Args:
        trip_line_id: UUID of the TripLine
        
    Returns:
        HTTP response with generated Word document
        
    URL: GET /api/documents/gendec/{trip_line_id}/
    """
    try:
        # Validate trip line exists
        trip_line = get_object_or_404(TripLine, id=trip_line_id)
        
        # Generate document
        generator = DocumentGenerator()
        response = generator.generate_gendec_response(str(trip_line_id))
        
        return response
        
    except TripLine.DoesNotExist:
        return Response(
            {'error': f'Trip line with ID {trip_line_id} not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except FileNotFoundError as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    except Exception as e:
        return Response(
            {'error': f'Error generating GenDec document: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generate_handling_request(request, trip_line_id):
    """
    Generate Handling Request document for a trip line.
    
    Args:
        trip_line_id: UUID of the TripLine
        
    Returns:
        HTTP response with generated Word document
        
    URL: GET /api/documents/handling-request/{trip_line_id}/
    """
    try:
        # Validate trip line exists
        trip_line = get_object_or_404(TripLine, id=trip_line_id)
        
        # Generate document
        generator = DocumentGenerator()
        response = generator.generate_handling_request_response(str(trip_line_id))
        
        return response
        
    except TripLine.DoesNotExist:
        return Response(
            {'error': f'Trip line with ID {trip_line_id} not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except FileNotFoundError as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    except Exception as e:
        return Response(
            {'error': f'Error generating Handling Request document: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generate_trip_documents(request, trip_id):
    """
    Generate both GenDec and Handling Request documents for all trip lines in a trip.
    Returns a ZIP file containing all generated documents.
    
    Args:
        trip_id: UUID of the Trip
        
    Returns:
        HTTP response with ZIP file containing all documents
        
    URL: GET /api/documents/trip/{trip_id}/
    """
    import zipfile
    import io
    from django.shortcuts import get_object_or_404
    from .models import Trip
    
    try:
        # Validate trip exists
        trip = get_object_or_404(Trip.objects.prefetch_related('trip_lines'), id=trip_id)
        
        # Create ZIP file in memory
        zip_buffer = io.BytesIO()
        generator = DocumentGenerator()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for trip_line in trip.trip_lines.all():
                try:
                    # Generate GenDec
                    gendec_data = generator._prepare_gendec_data(trip_line)
                    template_path = generator.templates_dir / "GenDec.docx"
                    if template_path.exists():
                        gendec_content = generator._generate_document_in_memory(template_path, gendec_data)
                        leg_suffix = f"{trip_line.origin_airport.iata_code}_{trip_line.destination_airport.iata_code}"
                        gendec_filename = f"GenDec_{trip.trip_number}_{leg_suffix}.docx"
                        zip_file.writestr(gendec_filename, gendec_content)
                    
                    # Generate Handling Request
                    hr_template_path = generator.templates_dir / "HandlingRequest.docx"
                    if hr_template_path.exists():
                        hr_content = generator._generate_document_in_memory(hr_template_path, gendec_data)
                        hr_filename = f"HandlingRequest_{trip.trip_number}_{leg_suffix}.docx"
                        zip_file.writestr(hr_filename, hr_content)
                        
                except Exception as e:
                    print(f"Error generating documents for trip line {trip_line.id}: {e}")
                    continue
        
        zip_buffer.seek(0)
        
        # Create HTTP response with ZIP file
        response = HttpResponse(
            zip_buffer.getvalue(),
            content_type='application/zip'
        )
        response['Content-Disposition'] = f'attachment; filename="Trip_{trip.trip_number}_Documents.zip"'
        
        return response
        
    except Trip.DoesNotExist:
        return Response(
            {'error': f'Trip with ID {trip_id} not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': f'Error generating trip documents: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def document_info(request):
    """
    Get information about available document types and templates.
    
    Returns:
        JSON response with document information
        
    URL: GET /api/documents/info/
    """
    generator = DocumentGenerator()
    
    # Check template availability
    templates_info = {
        'gendec': {
            'name': 'General Declaration',
            'template_exists': (generator.templates_dir / "GenDec.docx").exists(),
            'description': 'Aviation General Declaration document for flight legs'
        },
        'handling_request': {
            'name': 'Handling Request',
            'template_exists': (generator.templates_dir / "HandlingRequest.docx").exists(),
            'description': 'Ground handling service request document'
        }
    }
    
    return Response({
        'document_types': templates_info,
        'templates_directory': str(generator.templates_dir),
        'python_docx_available': generator._check_docx_availability()
    })


# Helper method for DocumentGenerator class
def _check_docx_availability(self):
    """Check if python-docx is available."""
    try:
        from docx import Document
        return True
    except ImportError:
        return False

# Add this method to DocumentGenerator class
DocumentGenerator._check_docx_availability = _check_docx_availability
