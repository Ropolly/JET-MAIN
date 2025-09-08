"""
DocuSeal API integration service for managing document signing workflows.
"""
import requests
import logging
from typing import Dict, List, Optional, Any
from django.conf import settings
from django.utils import timezone
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class DocuSealAPIError(Exception):
    """Custom exception for DocuSeal API errors."""
    pass


class DocuSealService:
    """
    Service class for integrating with DocuSeal API.
    Handles template creation, submission management, and webhook processing.
    """
    
    def __init__(self):
        self.api_key = getattr(settings, 'DOCUSEAL_API_KEY', None)
        self.base_url = getattr(settings, 'DOCUSEAL_BASE_URL', 'https://api.docuseal.com')
        
        if not self.api_key:
            logger.error("DocuSeal API key not configured")
            raise DocuSealAPIError("DocuSeal API key not configured")
    
    def _get_headers(self) -> Dict[str, str]:
        """Get standard headers for DocuSeal API requests."""
        return {
            'X-Auth-Token': self.api_key,
            'Content-Type': 'application/json'
        }
    
    def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        data: Optional[Dict] = None, 
        params: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Make HTTP request to DocuSeal API with error handling.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint path
            data: Request body data
            params: URL query parameters
            
        Returns:
            Dict containing API response data
            
        Raises:
            DocuSealAPIError: If API request fails
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self._get_headers(),
                json=data,
                params=params,
                timeout=30
            )
            
            # Log the response for debugging
            logger.info(f"DocuSeal API {method} {url} -> {response.status_code}")
            
            if not response.ok:
                error_details = ""
                try:
                    error_data = response.json()
                    error_details = f" - {error_data}"
                except:
                    error_details = f" - {response.text}"
                
                error_msg = f"DocuSeal API request failed: {response.status_code} {response.reason}{error_details}"
                logger.error(error_msg)
                raise DocuSealAPIError(error_msg)
            
            # Handle empty responses
            if response.status_code == 204:
                return {}
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            error_msg = f"DocuSeal API request failed: {str(e)}"
            logger.error(error_msg)
            raise DocuSealAPIError(error_msg) from e
        except ValueError as e:
            error_msg = f"Failed to parse DocuSeal API response: {str(e)}"
            logger.error(error_msg)
            raise DocuSealAPIError(error_msg) from e
    
    def create_template_from_html(
        self, 
        name: str, 
        html_content: str, 
        fields: List[Dict] = None
    ) -> Dict[str, Any]:
        """
        Create a DocuSeal template from HTML content.
        
        Args:
            name: Template name
            html_content: HTML content for the template
            fields: List of form fields for the template
            
        Returns:
            Dict containing template information including template ID
        """
        data = {
            'name': name,
            'html': html_content
        }
        
        if fields:
            data['fields'] = fields
        
        logger.info(f"Creating DocuSeal template: {name}")
        return self._make_request('POST', '/templates', data=data)
    
    def create_template_from_pdf(
        self, 
        name: str, 
        pdf_content: bytes, 
        filename: str
    ) -> Dict[str, Any]:
        """
        Create a DocuSeal template from PDF content.
        
        Args:
            name: Template name
            pdf_content: PDF file content as bytes
            filename: Original filename
            
        Returns:
            Dict containing template information including template ID
        """
        # For PDF uploads, we need to use multipart/form-data
        files = {
            'file': (filename, pdf_content, 'application/pdf')
        }
        
        form_data = {
            'name': name
        }
        
        url = f"{self.base_url}/templates"
        
        try:
            response = requests.post(
                url=url,
                headers={'X-Auth-Token': self.api_key},
                files=files,
                data=form_data,
                timeout=30
            )
            
            response.raise_for_status()
            logger.info(f"Created DocuSeal template from PDF: {name}")
            return response.json()
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Failed to upload PDF template: {str(e)}"
            logger.error(error_msg)
            raise DocuSealAPIError(error_msg) from e
    
    def create_submission(
        self,
        template_id: str,
        submitters: List[Dict[str, Any]],
        send_email: bool = True,
        completed_redirect_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a submission (signature request) from a template.
        
        Args:
            template_id: DocuSeal template ID
            submitters: List of submitter information (with fields as dict)
            send_email: Whether to send email notifications
            completed_redirect_url: URL to redirect after completion
            
        Returns:
            Dict containing submission information including submission ID
        """
        # Convert submitters format - DocuSeal expects fields as array of objects
        formatted_submitters = []
        for submitter in submitters:
            formatted_submitter = {
                'name': submitter['name'],
                'email': submitter['email']
            }
            
            # Add role if provided
            if 'role' in submitter:
                formatted_submitter['role'] = submitter['role']
            
            # Convert fields dict to array format expected by DocuSeal
            if 'fields' in submitter and submitter['fields']:
                formatted_submitter['fields'] = [
                    {'name': field_name, 'default_value': field_value}
                    for field_name, field_value in submitter['fields'].items()
                    if field_value  # Only include fields with values
                ]
            else:
                formatted_submitter['fields'] = []
            
            formatted_submitters.append(formatted_submitter)
        
        data = {
            'template_id': int(template_id),
            'submitters': formatted_submitters,
            'send_email': send_email
        }
        
        if completed_redirect_url:
            data['completed_redirect_url'] = completed_redirect_url
        
        logger.info(f"Creating DocuSeal submission for template: {template_id}")
        logger.info(f"Formatted submission data: {data}")
        
        try:
            return self._make_request('POST', '/submissions', data=data)
        except Exception as e:
            logger.error(f"Submission creation failed. Data sent: {data}")
            raise e
    
    def get_submission(self, submission_id: str) -> Dict[str, Any]:
        """
        Get submission details by ID.
        
        Args:
            submission_id: DocuSeal submission ID
            
        Returns:
            Dict containing submission details and status
        """
        logger.info(f"Fetching DocuSeal submission: {submission_id}")
        return self._make_request('GET', f'/submissions/{submission_id}')
    
    def list_submissions(
        self, 
        template_id: Optional[str] = None,
        limit: int = 100,
        after: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        List submissions with optional filtering.
        
        Args:
            template_id: Filter by template ID
            limit: Number of submissions to return
            after: Pagination cursor
            
        Returns:
            Dict containing list of submissions and pagination info
        """
        params = {'limit': limit}
        
        if template_id:
            params['template_id'] = template_id
        if after:
            params['after'] = after
        
        return self._make_request('GET', '/submissions', params=params)
    
    def get_submission_documents(self, submission_id: str) -> bytes:
        """
        Download completed/signed documents for a submission.
        
        Args:
            submission_id: DocuSeal submission ID
            
        Returns:
            PDF document content as bytes
        """
        url = f"{self.base_url}/submissions/{submission_id}/documents"
        
        try:
            response = requests.get(
                url=url,
                headers={'X-Auth-Token': self.api_key},
                timeout=30
            )
            
            response.raise_for_status()
            logger.info(f"Downloaded documents for submission: {submission_id}")
            return response.content
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Failed to download submission documents: {str(e)}"
            logger.error(error_msg)
            raise DocuSealAPIError(error_msg) from e
    
    def archive_submission(self, submission_id: str) -> Dict[str, Any]:
        """
        Archive a submission.
        
        Args:
            submission_id: DocuSeal submission ID
            
        Returns:
            Dict containing archived submission info
        """
        logger.info(f"Archiving DocuSeal submission: {submission_id}")
        return self._make_request('DELETE', f'/submissions/{submission_id}')
    
    def process_webhook_event(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process incoming webhook event from DocuSeal.
        
        Args:
            webhook_data: Webhook payload from DocuSeal
            
        Returns:
            Dict containing processed event information
        """
        event_type = webhook_data.get('event_type')
        submission_data = webhook_data.get('data', {})
        submission_id = submission_data.get('id')
        
        logger.info(f"Processing DocuSeal webhook: {event_type} for submission {submission_id}")
        
        return {
            'event_type': event_type,
            'submission_id': submission_id,
            'submission_data': submission_data,
            'processed_at': timezone.now().isoformat()
        }
    
    def create_contract_fields_mapping(
        self, 
        contract_type: str,
        trip_data: Dict, 
        trip_lines_data: List[Dict] = None,
        contact_data: Dict = None, 
        patient_data: Dict = None,
        passengers_data: List[Dict] = None,
        quote_data: Dict = None
    ) -> Dict[str, Any]:
        """
        Create field mappings for specific contract templates based on contract type.
        
        Args:
            contract_type: Type of contract (consent_transport, payment_agreement, patient_service_agreement)
            trip_data: Trip information dictionary
            trip_lines_data: List of trip line data (can be dicts or objects)
            contact_data: Contact/customer information dictionary  
            patient_data: Patient information dictionary
            passengers_data: List of passenger information
            quote_data: Quote information dictionary
            
        Returns:
            Dict containing field mappings for DocuSeal template
        """
        from datetime import datetime
        
        # Get origin and destination airports from trip lines
        from_airport = ''
        to_airport = ''
        if trip_lines_data and len(trip_lines_data) > 0:
            # Handle both dict and object formats
            first_line = trip_lines_data[0]
            last_line = trip_lines_data[-1]
            
            if hasattr(first_line, 'origin_airport'):
                # Object format
                from_airport = first_line.origin_airport.name if first_line.origin_airport else ''
                to_airport = last_line.destination_airport.name if last_line.destination_airport else ''
            else:
                # Dict format - try different possible field names
                from_airport = first_line.get('origin_airport_name', '') or first_line.get('origin_airport', '')
                to_airport = last_line.get('destination_airport_name', '') or last_line.get('destination_airport', '')
        
        # Calculate price with 2.5% fee if quote data available
        price_with_fee = ''
        if quote_data and quote_data.get('quoted_amount'):
            base_price = float(quote_data.get('quoted_amount', 0))
            price_with_fee = f"${base_price * 1.025:,.2f}"
        
        # Get patient name
        patient_name = ''
        patient_phone = ''
        patient_address = ''
        patient_csz = ''  # City, State, Zip
        if patient_data:
            patient_info = patient_data.get('info', {})
            patient_first = patient_info.get('first_name', '')
            patient_last = patient_info.get('last_name', '')
            patient_name = f"{patient_first} {patient_last}".strip()
            patient_phone = patient_info.get('phone', '')
            patient_address = patient_info.get('address_line1', '')
            
            # Build city, state, zip
            city = patient_info.get('city', '')
            state = patient_info.get('state', '')
            zip_code = patient_info.get('zip', '')
            patient_csz = f"{city}, {state} {zip_code}".strip()
        
        # Get customer name and email
        customer_name = ''
        customer_email = ''
        if contact_data:
            customer_first = contact_data.get('first_name', '')
            customer_last = contact_data.get('last_name', '')
            customer_name = f"{customer_first} {customer_last}".strip()
            if not customer_name and contact_data.get('business_name'):
                customer_name = contact_data.get('business_name', '')
            customer_email = contact_data.get('email', '')
        
        # Get passenger names (first passenger if any)
        passenger_name = 'None'
        if passengers_data and len(passengers_data) > 0:
            passenger_info = passengers_data[0].get('info', {})
            passenger_first = passenger_info.get('first_name', '')
            passenger_last = passenger_info.get('last_name', '')
            passenger_full = f"{passenger_first} {passenger_last}".strip()
            if passenger_full:
                passenger_name = passenger_full
        
        # Get current date components
        now = timezone.now()
        day_number = now.strftime('%d').lstrip('0')  # Remove leading zero
        month_name = now.strftime('%B')  # Full month name like "August"
        
        # Build field mappings based on contract type
        if contract_type == 'consent_transport':
            # Consent for Transport fields
            return {
                'from_airport': from_airport,
                'to_airport': to_airport,
            }
        
        elif contract_type == 'payment_agreement':
            # Air Ambulance Payment Agreement fields
            return {
                'patient_name': patient_name,
                'passenger_name': passenger_name,
                'from_airport': from_airport,
                'to_airport': to_airport,
                'price': price_with_fee,
                'customer_name': customer_name,
                'customer_email': customer_email,
            }
        
        elif contract_type == 'patient_service_agreement':
            # Patient Service Agreement fields
            return {
                'day_number': day_number,
                'month_name': month_name,
                'patient_name': patient_name,
                'patient_phone': patient_phone,
                'patient_address': patient_address,
                'patient_csz': patient_csz,
                'from_airport': from_airport,
                'to_airport': to_airport,
            }
        
        else:
            # Default fields for unknown contract types
            return {
                'from_airport': from_airport,
                'to_airport': to_airport,
                'customer_name': customer_name,
                'customer_email': customer_email,
                'patient_name': patient_name,
            }