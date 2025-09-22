from django.shortcuts import render
from rest_framework import viewsets, permissions, status, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Q
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.conf import settings
import json
import os
import uuid
from datetime import datetime
from itertools import chain
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from io import BytesIO
import logging
from .decorators import is_hipaa_protected
# TripEvent imports moved to consolidated imports section below

from .external.airport import get_airport, parse_fuel_cost

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_fuel_prices(request, airport_code):
    """
    Get fuel prices for a specific airport
    """
    try:
        # Get airport data from FlightAware
        soup = get_airport(airport_code)
        if not soup:
            return JsonResponse({'error': 'Failed to retrieve airport data'}, status=400)
        
        # Parse fuel prices
        fuel_prices = parse_fuel_cost(soup)
        
        return JsonResponse({'fuel_prices': fuel_prices})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

from .models import (
    Modification, Permission, Role, Department, UserProfile, Contact, 
    FBO, Ground, Airport, Document, Aircraft, Transaction, Agreement,
    Patient, Quote, Passenger, CrewLine, Trip, TripLine, Staff, StaffRole, StaffRoleMembership, TripEvent, Comment, Contract, LostReason
)
from .utils import track_creation, track_deletion
from .contact_service import ContactCreationService, ContactCreationSerializer
from utils.services.docuseal_service import DocuSealService

logger = logging.getLogger(__name__)
from .serializers import (
    ModificationSerializer, PermissionSerializer, RoleSerializer, DepartmentSerializer,
    ContactReadSerializer, ContactWriteSerializer, CommentSerializer, FBOSerializer, GroundSerializer, AirportSerializer, AircraftSerializer,
    AgreementSerializer, DocumentSerializer, LostReasonSerializer,
    # Standardized CRUD serializers
    UserProfileReadSerializer, UserProfileWriteSerializer,
    PassengerReadSerializer, PassengerWriteSerializer,
    CrewLineReadSerializer, CrewLineWriteSerializer,
    TripLineReadSerializer, TripLineWriteSerializer,
    TripEventReadSerializer, TripEventWriteSerializer,
    TripReadSerializer, TripWriteSerializer,
    QuoteReadSerializer, QuoteWriteSerializer,
    DocumentReadSerializer, DocumentUploadSerializer,
    TransactionPublicReadSerializer, TransactionReadSerializer, TransactionProcessWriteSerializer,
    PatientReadSerializer, PatientWriteSerializer, PatientFileUploadSerializer, StaffReadSerializer, StaffWriteSerializer,
    StaffRoleSerializer,
    StaffRoleMembershipReadSerializer, StaffRoleMembershipWriteSerializer,
    ContractReadSerializer, ContractWriteSerializer, ContractCreateFromTripSerializer,
    ContractDocuSealActionSerializer, DocuSealWebhookSerializer,
)
from .permissions import (
    IsAuthenticatedOrPublicEndpoint, IsTransactionOwner,
    CanReadQuote, CanWriteQuote, CanModifyQuote, CanDeleteQuote,
    CanReadPatient, CanWritePatient, CanModifyPatient, CanDeletePatient,
    CanReadTrip, CanWriteTrip, CanModifyTrip, CanDeleteTrip,
    CanReadPassenger, CanWritePassenger, CanModifyPassenger, CanDeletePassenger,
    CanReadTransaction, CanWriteTransaction, CanModifyTransaction, CanDeleteTransaction,
    CanReadTripLine, CanWriteTripLine, CanModifyTripLine, CanDeleteTripLine
)

# Standard pagination class for all ViewSets
class StandardPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 100

# Custom pagination for airports (if different settings needed)
class AirportPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 100

# Base ViewSet with common functionality
class BaseViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardPagination  # Apply pagination to all ViewSets
    
    def perform_create(self, serializer):
        instance = serializer.save(created_by=self.request.user)
        # Track creation
        track_creation(instance, self.request.user)
    
    def perform_update(self, serializer):
        from .signals import set_skip_signal_tracking
        
        # Get the old instance before updating
        if serializer.instance and hasattr(serializer.instance, 'pk'):
            old_instance = serializer.instance.__class__.objects.get(pk=serializer.instance.pk)
            # Exclude system fields and encrypted PHI fields that shouldn't be tracked
            excluded_fields = {'id', 'created_on', 'modified_on', 'created_by', 'modified_by'}
            old_fields = {}
            for field in old_instance._meta.fields:
                if (not field.is_relation and
                    field.name not in excluded_fields and
                    not field.name.endswith('_encrypted') and
                    not field.name.endswith('_hash')):
                    old_fields[field.name] = getattr(old_instance, field.name)
        else:
            old_fields = {}
        
        try:
            # Skip signal tracking during this operation
            set_skip_signal_tracking(True)
            
            # Save the instance
            instance = serializer.save(modified_by=self.request.user)
            
        finally:
            # Re-enable signal tracking
            set_skip_signal_tracking(False)
        
        # Track modifications manually with user
        if old_fields:
            from .utils import track_modification
            # Use same excluded fields for new values (including encrypted PHI fields)
            excluded_fields = {'id', 'created_on', 'modified_on', 'created_by', 'modified_by'}
            new_fields = {}
            for field in instance._meta.fields:
                if (not field.is_relation and
                    field.name not in excluded_fields and
                    not field.name.endswith('_encrypted') and
                    not field.name.endswith('_hash')):
                    new_fields[field.name] = getattr(instance, field.name)

            for field_name, old_value in old_fields.items():
                new_value = new_fields.get(field_name)
                if old_value != new_value:
                    track_modification(instance, field_name, old_value, new_value, self.request.user)
        
    def perform_destroy(self, instance):
        # Track deletion before destroying
        track_deletion(instance, self.request.user)
        instance.delete()

# Permission ViewSet
class PermissionViewSet(BaseViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_on']

# Role ViewSet
class RoleViewSet(BaseViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_on']

# Department ViewSet
class DepartmentViewSet(BaseViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_on']

# UserProfile ViewSet
class UserProfileViewSet(BaseViewSet):
    queryset = UserProfile.objects.select_related('user').prefetch_related('roles', 'departments')
    search_fields = ['first_name', 'last_name', 'email']
    ordering_fields = ['first_name', 'last_name', 'created_on']
    
    def get_serializer_class(self):
        if self.action in ('list', 'retrieve', 'me'):
            return UserProfileReadSerializer
        return UserProfileWriteSerializer
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        try:
            profile = UserProfile.objects.select_related('user').prefetch_related('roles', 'departments').get(user=request.user)
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response({"detail": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

# Contact ViewSet
class ContactViewSet(BaseViewSet):
    queryset = Contact.objects.all()
    search_fields = ['first_name', 'last_name', 'business_name', 'email']
    ordering_fields = ['first_name', 'last_name', 'business_name', 'created_on']

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return ContactReadSerializer
        return ContactWriteSerializer

# FBO ViewSet
class FBOViewSet(BaseViewSet):
    queryset = FBO.objects.all()
    serializer_class = FBOSerializer
    search_fields = ['name', 'city', 'country']
    ordering_fields = ['name', 'created_on']

# Ground ViewSet
class GroundViewSet(BaseViewSet):
    queryset = Ground.objects.all()
    serializer_class = GroundSerializer
    search_fields = ['name', 'city', 'country']
    ordering_fields = ['name', 'created_on']

# Airport ViewSet
class AirportViewSet(BaseViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    pagination_class = AirportPagination
    search_fields = ['name', 'ident', 'icao_code', 'iata_code', 'municipality', 'iso_country', 'iso_region']
    ordering_fields = ['name', 'ident', 'icao_code', 'iata_code', 'airport_type', 'created_on']
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')
        if len(query) < 2:
            return Response({"detail": "Search query too short"}, status=status.HTTP_400_BAD_REQUEST)
            
        airports = Airport.objects.filter(
            Q(name__icontains=query) | 
            Q(ident__icontains=query) |
            Q(icao_code__icontains=query) | 
            Q(iata_code__icontains=query) |
            Q(municipality__icontains=query) |
            Q(iso_country__icontains=query)
        )[:10]
        
        serializer = self.get_serializer(airports, many=True)
        return Response(serializer.data)

# Document ViewSet
class DocumentViewSet(BaseViewSet):
    queryset = Document.objects.all()
    
    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return DocumentUploadSerializer
        return DocumentReadSerializer
    
    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        document = self.get_object()
        response = HttpResponse(document.content, content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{document.filename}"'
        return response

# Aircraft ViewSet
class AircraftViewSet(BaseViewSet):
    queryset = Aircraft.objects.all()
    serializer_class = AircraftSerializer
    search_fields = ['tail_number', 'make', 'model', 'company']
    ordering_fields = ['tail_number', 'make', 'model', 'created_on']

# Transaction ViewSet
class TransactionViewSet(BaseViewSet):
    queryset = Transaction.objects.all()
    search_fields = ['key', 'email', 'payment_status']
    ordering_fields = ['payment_date', 'amount', 'created_on']
    permission_classes = [
        IsAuthenticatedOrPublicEndpoint, 
        IsTransactionOwner,
        CanReadTransaction | CanWriteTransaction | CanModifyTransaction | CanDeleteTransaction
    ]
    public_actions = ['retrieve_by_key']
    
    def get_serializer_class(self):
        # Public read by key uses minimal serializer
        if self.action == 'retrieve_by_key':
            return TransactionPublicReadSerializer
        # Staff read operations use full serializer
        elif self.action in ('list', 'retrieve'):
            return TransactionReadSerializer
        # Process payment uses special write serializer
        elif self.action == 'process_payment':
            return TransactionProcessWriteSerializer
        # Default write operations
        return TransactionProcessWriteSerializer
    
    @action(detail=False, methods=['get'], url_path='pay/(?P<transaction_key>[^/.]+)')
    def retrieve_by_key(self, request, transaction_key=None):
        """
        Public endpoint to retrieve transaction details by key for payment processing.
        """
        try:
            transaction = Transaction.objects.get(key=transaction_key)
            serializer = self.get_serializer(transaction)
            return Response(serializer.data)
        except Transaction.DoesNotExist:
            return Response(
                {"detail": "Transaction not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'])
    def process_payment(self, request, pk=None):
        transaction = self.get_object()
        # Here you would integrate with Authorize.net
        # This is a placeholder for the actual payment processing logic
        transaction.payment_status = "completed"
        transaction.save()
        serializer = self.get_serializer(transaction)
        return Response(serializer.data)

# Agreement ViewSet
class AgreementViewSet(BaseViewSet):
    queryset = Agreement.objects.all()
    serializer_class = AgreementSerializer
    search_fields = ['destination_email', 'status']
    ordering_fields = ['created_on', 'status']
    
    @action(detail=True, methods=['post'])
    def send_for_signature(self, request, pk=None):
        agreement = self.get_object()
        # Here you would integrate with Adobe Sign
        # This is a placeholder for the actual signature request logic
        agreement.status = "pending"
        agreement.save()
        serializer = self.get_serializer(agreement)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def check_signature_status(self, request, pk=None):
        agreement = self.get_object()
        # Here you would check with Adobe Sign API
        # This is a placeholder for the actual status check logic
        serializer = self.get_serializer(agreement)
        return Response(serializer.data)

# Patient ViewSet
@is_hipaa_protected()
class PatientViewSet(BaseViewSet):
    queryset = Patient.objects.select_related('info')
    # Remove search_fields to prevent DRF SearchFilter from interfering with our custom search
    # search_fields = ['info__first_name', 'info__last_name', 'nationality']
    ordering_fields = ['created_on']
    permission_classes = [
        permissions.IsAuthenticated,
        CanReadPatient | CanWritePatient | CanModifyPatient | CanDeletePatient
    ]

    # Override filter_backends to exclude SearchFilter since we handle search in get_queryset
    from django_filters.rest_framework import DjangoFilterBackend
    from rest_framework.filters import OrderingFilter
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    
    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return PatientReadSerializer
        return PatientWriteSerializer
    
    def get_permissions(self):
        """
        Instantiate and return the list of permissions that this view requires.
        """
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [permissions.IsAuthenticated, CanReadPatient]
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated, CanWritePatient]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [permissions.IsAuthenticated, CanModifyPatient]
        elif self.action == 'destroy':
            permission_classes = [permissions.IsAuthenticated, CanDeletePatient]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        Override to handle encrypted search functionality.
        """
        queryset = super().get_queryset()
        search = self.request.query_params.get('search')

        if search:
            # For encrypted search, we need to handle both legacy data and encrypted data
            from django.db.models import Q
            from .encryption import FieldEncryption

            # Search legacy fields (for existing data)
            legacy_search = Q()
            legacy_search |= Q(info__first_name__icontains=search)
            legacy_search |= Q(info__last_name__icontains=search)
            legacy_search |= Q(nationality__icontains=search)

            # Get legacy results
            legacy_results = queryset.filter(legacy_search)
            legacy_ids = set(legacy_results.values_list('id', flat=True))

            # Search encrypted fields for ALL patients (not just when legacy is empty)
            # Get all patients and check encrypted fields manually
            all_patients = Patient.objects.select_related('info').all()
            encrypted_matching_ids = []

            for patient in all_patients:
                # Skip if already found in legacy search
                if patient.id in legacy_ids:
                    continue

                # Check if contact info matches (encrypted data)
                contact_matches = False
                if patient.info:
                    contact_first_name = patient.info.get_first_name().lower()
                    contact_last_name = patient.info.get_last_name().lower()
                    if (search.lower() in contact_first_name or
                        search.lower() in contact_last_name):
                        contact_matches = True

                # Check patient nationality (encrypted data)
                patient_nationality = patient.get_nationality().lower()
                nationality_matches = search.lower() in patient_nationality

                if contact_matches or nationality_matches:
                    encrypted_matching_ids.append(patient.id)

            # Combine legacy and encrypted results
            all_matching_ids = list(legacy_ids) + encrypted_matching_ids

            if all_matching_ids:
                queryset = Patient.objects.filter(id__in=all_matching_ids).select_related('info')
            else:
                # No matches found in either legacy or encrypted data
                queryset = Patient.objects.none()

        return queryset

    @action(detail=True, methods=['post'], parser_classes=[MultiPartParser, FormParser])
    def upload_document(self, request, pk=None):
        """Upload a document (insurance card or letter of medical necessity) for a patient"""
        patient = self.get_object()
        serializer = PatientFileUploadSerializer(data=request.data)
        
        if serializer.is_valid():
            file = serializer.validated_data['file']
            document_type = serializer.validated_data['document_type']
            trip_id = serializer.validated_data.get('trip_id')
            
            # Validate file type
            allowed_extensions = ['.jpg', '.jpeg', '.png', '.pdf']
            file_extension = os.path.splitext(file.name)[1].lower()
            if file_extension not in allowed_extensions:
                return Response(
                    {'error': 'Only JPG, PNG, and PDF files are allowed'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Validate file size (10MB limit)
            if file.size > 10 * 1024 * 1024:
                return Response(
                    {'error': 'File size cannot exceed 10MB'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                # Create upload directory if it doesn't exist
                upload_dir = os.path.join(settings.MEDIA_ROOT, 'patient_documents')
                os.makedirs(upload_dir, exist_ok=True)
                
                # Get or create trip reference if provided
                trip = None
                if trip_id:
                    try:
                        trip = Trip.objects.get(id=trip_id)
                    except Trip.DoesNotExist:
                        return Response(
                            {'error': 'Trip not found'},
                            status=status.HTTP_404_NOT_FOUND
                        )

                # Generate descriptive filename with unit prefix
                # Get trip number if available
                unit_prefix = ""
                if trip and trip.trip_number:
                    unit_prefix = f"{trip.trip_number}_"

                # Create descriptive filename
                if document_type == 'insurance_card':
                    descriptive_name = f"{unit_prefix}Insurance_Card"
                elif document_type == 'letter_of_medical_necessity':
                    descriptive_name = f"{unit_prefix}Letter_of_Medical_Necessity"
                else:
                    descriptive_name = f"{unit_prefix}{document_type}"

                # Add timestamp for uniqueness
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{descriptive_name}_{timestamp}{file_extension}"
                file_path = os.path.join(upload_dir, filename)
                
                # Save file
                with open(file_path, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
                
                
                # Create document record
                document = Document.objects.create(
                    filename=filename,
                    document_type=document_type,
                    file_path=f"patient_documents/{filename}",
                    trip=trip,
                    patient=patient,
                    created_by=request.user
                )
                
                # Update patient with document reference
                if document_type == 'insurance_card':
                    patient.insurance_card = document
                    patient.save()
                elif document_type == 'letter_of_medical_necessity':
                    patient.letter_of_medical_necessity = document
                    patient.save()
                
                return Response({
                    'message': 'Document uploaded successfully',
                    'document_id': document.id,
                    'file_path': document.file_path
                }, status=status.HTTP_201_CREATED)
                
            except Exception as e:
                return Response(
                    {'error': f'Failed to upload file: {str(e)}'}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def delete_document(self, request, pk=None):
        """Delete a document for a patient"""
        patient = self.get_object()
        document_type = request.query_params.get('document_type')
        
        if not document_type:
            return Response(
                {'error': 'document_type parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if document_type not in ['insurance_card', 'letter_of_medical_necessity']:
            return Response(
                {'error': 'Invalid document_type'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            if document_type == 'insurance_card' and patient.insurance_card:
                document = patient.insurance_card
                
                # Delete physical file
                if document.file_path:
                    file_path = os.path.join(settings.MEDIA_ROOT, document.file_path)
                    if os.path.exists(file_path):
                        os.remove(file_path)
                
                # Remove reference from patient
                patient.insurance_card = None
                patient.save()
                
                # Delete document record
                document.delete()
                
                return Response({'message': 'Document deleted successfully'})
            
            elif document_type == 'letter_of_medical_necessity':
                # Find letter of medical necessity documents for this patient
                trip_id = request.query_params.get('trip_id')
                if trip_id:
                    documents = Document.objects.filter(
                        document_type='letter_of_medical_necessity',
                        trip_id=trip_id
                    )
                else:
                    # If no trip_id provided, we can't identify which document to delete
                    return Response(
                        {'error': 'trip_id parameter is required for letter_of_medical_necessity'}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                if not documents.exists():
                    return Response(
                        {'error': 'Document not found'}, 
                        status=status.HTTP_404_NOT_FOUND
                    )
                
                # Delete all matching documents
                for document in documents:
                    if document.file_path:
                        file_path = os.path.join(settings.MEDIA_ROOT, document.file_path)
                        if os.path.exists(file_path):
                            os.remove(file_path)
                    document.delete()
                
                return Response({'message': 'Document(s) deleted successfully'})
            
            else:
                return Response(
                    {'error': 'No document found to delete'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
                
        except Exception as e:
            return Response(
                {'error': f'Failed to delete document: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# Quote ViewSet
class QuoteViewSet(BaseViewSet):
    queryset = Quote.objects.select_related('contact', 'pickup_airport', 'dropoff_airport', 'patient', 'patient__info').prefetch_related('transactions')
    search_fields = ['contact__first_name', 'contact__last_name', 'patient__info__first_name', 'patient__info__last_name', 'status']
    ordering_fields = ['created_on', 'quoted_amount']
    permission_classes = [
        permissions.IsAuthenticated,
        CanReadQuote | CanWriteQuote | CanModifyQuote | CanDeleteQuote
    ]
    
    def get_queryset(self):
        """
        Filter quotes by status and handle UUID search if provided in query params
        """
        queryset = super().get_queryset()
        
        # Filter by status if provided
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
            
        return queryset
    
    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return QuoteReadSerializer
        return QuoteWriteSerializer
    
    def get_permissions(self):
        """
        Instantiate and return the list of permissions that this view requires.
        """
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [permissions.IsAuthenticated, CanReadQuote]
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated, CanWriteQuote]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [permissions.IsAuthenticated, CanModifyQuote]
        elif self.action == 'destroy':
            permission_classes = [permissions.IsAuthenticated, CanDeleteQuote]
        elif self.action == 'create_transaction':
            permission_classes = [permissions.IsAuthenticated, CanWriteTransaction]
        elif self.action == 'generate_quote_document':
            permission_classes = [permissions.IsAuthenticated, CanModifyQuote]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @action(detail=True, methods=['post'])
    def create_transaction(self, request, pk=None):
        quote = self.get_object()
        amount = request.data.get('amount', quote.quoted_amount)
        email = request.data.get('email', quote.quote_pdf_email)
        
        transaction = Transaction.objects.create(
            created_by=request.user,
            amount=amount,
            payment_method=request.data.get('payment_method', 'credit_card'),
            email=email
        )
        
        quote.transactions.add(transaction)
        
        return Response(TransactionReadSerializer(transaction).data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['get'])
    def pdf(self, request, pk=None):
        """
        Generate and return a professional quote PDF
        """
        quote = self.get_object()
        
        # Generate PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer, 
            pagesize=letter, 
            rightMargin=50, 
            leftMargin=50, 
            topMargin=50, 
            bottomMargin=50
        )
        
        # Custom styles
        styles = getSampleStyleSheet()
        
        # Company header style
        company_style = ParagraphStyle(
            'CompanyHeader',
            parent=styles['Normal'],
            fontSize=18,
            fontName='Helvetica-Bold',
            textColor=colors.HexColor('#1E40AF'),
            alignment=0,  # Left alignment
            spaceBefore=0,
            spaceAfter=6,
            leading=22
        )
        
        # Company info style
        company_info_style = ParagraphStyle(
            'CompanyInfo',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#6B7280'),
            alignment=0,
            spaceBefore=0,
            spaceAfter=0,
            leading=11
        )
        
        # Quote title style
        quote_title_style = ParagraphStyle(
            'QuoteTitle',
            parent=styles['Normal'],
            fontSize=24,
            fontName='Helvetica-Bold',
            textColor=colors.HexColor('#1F2937'),
            alignment=2,  # Right alignment
            spaceBefore=0,
            spaceAfter=6,
            leading=28
        )
        
        # Quote number style
        quote_number_style = ParagraphStyle(
            'QuoteNumber',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#6B7280'),
            alignment=2,  # Right alignment
            spaceBefore=0,
            spaceAfter=0,
            leading=12
        )
        
        # Section header style
        section_header_style = ParagraphStyle(
            'SectionHeader',
            parent=styles['Normal'],
            fontSize=11,
            fontName='Helvetica-Bold',
            textColor=colors.HexColor('#1F2937'),
            spaceBefore=25,
            spaceAfter=12,
            leading=13,
            leftIndent=0,
            rightIndent=0
        )
        
        # Build PDF content
        story = []
        
        # Header section with company info and quote title
        header_data = [
            [
                Paragraph("JET ICU MEDICAL TRANSPORT", company_style), 
                Paragraph("QUOTE", quote_title_style)
            ],
            [
                Paragraph("1511 N Westshore Blvd #650<br/>Tampa, FL 33607", company_info_style),
                Paragraph(f"#{quote.id.hex[:8].upper()}", quote_number_style)
            ],
            [
                Paragraph("Phone: (352) 796-2540<br/>Email: info@jeticu.com", company_info_style),
                Paragraph(f"Date: {quote.created_on.strftime('%B %d, %Y') if quote.created_on else 'N/A'}", quote_number_style)
            ]
        ]
        
        header_table = Table(header_data, colWidths=[4.2*inch, 2.3*inch])
        header_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ]))
        
        story.append(header_table)
        story.append(Spacer(1, 25))
        
        # Add customer info style
        customer_info_style = ParagraphStyle(
            'CustomerInfo',
            parent=styles['Normal'],
            fontSize=10,
            leading=14,
            spaceBefore=0,
            spaceAfter=0,
            leftIndent=0,
            rightIndent=0
        )
        
        # Bill To section
        if quote.contact:
            story.append(Paragraph("BILL TO", section_header_style))
            
            # Customer details
            customer_lines = []
            
            # Name and business
            name = f"{quote.contact.first_name} {quote.contact.last_name}"
            if quote.contact.business_name:
                customer_lines.append(quote.contact.business_name)
                customer_lines.append(name)
            else:
                customer_lines.append(name)
            
            # Address
            if quote.contact.address_line1:
                customer_lines.append(quote.contact.address_line1)
            if quote.contact.address_line2:
                customer_lines.append(quote.contact.address_line2)
            if quote.contact.city:
                city_line = quote.contact.city
                if quote.contact.state:
                    city_line += f", {quote.contact.state}"
                if quote.contact.zip:
                    city_line += f" {quote.contact.zip}"
                customer_lines.append(city_line)
            
            # Contact info
            if quote.contact.email:
                customer_lines.append(f"Email: {quote.contact.email}")
            if quote.contact.phone:
                customer_lines.append(f"Phone: {quote.contact.phone}")
            
            story.append(Paragraph("<br/>".join(customer_lines), customer_info_style))
            story.append(Spacer(1, 25))
        
        # Service Details Section
        story.append(Paragraph("SERVICE DETAILS", section_header_style))
        
        # Service table
        service_data = [
            ['Service', 'Details', 'Amount'],
        ]
        
        # Aircraft type description
        aircraft_desc = dict(quote._meta.get_field('aircraft_type').choices).get(quote.aircraft_type, quote.aircraft_type)
        medical_desc = dict(quote._meta.get_field('medical_team').choices).get(quote.medical_team, quote.medical_team)
        
        # Route description
        route = "Medical Air Transport"
        if quote.pickup_airport and quote.dropoff_airport:
            route = f"{quote.pickup_airport.name} → {quote.dropoff_airport.name}"
        
        service_data.append([
            route,
            f"Aircraft: {aircraft_desc}<br/>Medical Team: {medical_desc}<br/>Flight Time: {quote.estimated_flight_time if quote.estimated_flight_time else 'TBD'}",
            f"${quote.quoted_amount:,.2f}"
        ])
        
        # Ground transport if included
        if quote.includes_grounds:
            service_data.append([
                "Ground Transportation",
                "Airport transfers included",
                "Included"
            ])
        
        # Service table with better column distribution
        service_table = Table(service_data, colWidths=[2.2*inch, 2.8*inch, 1.5*inch])
        service_table.setStyle(TableStyle([
            # Header row
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1F2937')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
            
            # Data rows
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),      # Service column
            ('ALIGN', (1, 1), (1, -1), 'LEFT'),      # Details column
            ('ALIGN', (2, 1), (2, -1), 'RIGHT'),     # Amount column
            ('VALIGN', (0, 1), (-1, -1), 'TOP'),
            
            # Alternating row colors
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F9FAFB')]),
            
            # Grid
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E5E7EB')),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.HexColor('#1F2937')),
            
            # Padding - increased for better spacing
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        story.append(service_table)
        story.append(Spacer(1, 25))
        
        # Total section
        total_data = [
            ['', 'Subtotal:', f"${quote.quoted_amount:,.2f}"],
            ['', 'Tax:', "$0.00"],
            ['', 'TOTAL:', f"${quote.quoted_amount:,.2f}"]
        ]
        
        total_table = Table(total_data, colWidths=[3.2*inch, 1.6*inch, 1.7*inch])
        total_table.setStyle(TableStyle([
            ('FONTNAME', (1, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (1, 0), (-1, 1), 10),
            ('FONTSIZE', (1, 2), (-1, 2), 12),  # Total row larger
            ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
            ('TEXTCOLOR', (1, 2), (-1, 2), colors.HexColor('#1F2937')),
            ('LINEABOVE', (1, 2), (-1, 2), 1.5, colors.HexColor('#1F2937')),
            ('TOPPADDING', (1, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (1, 0), (-1, -1), 6),
            ('LEFTPADDING', (1, 0), (-1, -1), 4),
            ('RIGHTPADDING', (1, 0), (-1, -1), 4),
        ]))
        
        story.append(total_table)
        story.append(Spacer(1, 25))
        
        # Patient Information (if applicable)
        if quote.patient and quote.patient.info:
            story.append(Paragraph("PATIENT INFORMATION", section_header_style))
            
            patient_info_data = [
                ['Patient Name:', f"{quote.patient.info.first_name} {quote.patient.info.last_name}"],
            ]
            
            if quote.patient.info.date_of_birth:
                patient_info_data.append(['Date of Birth:', quote.patient.info.date_of_birth.strftime('%B %d, %Y')])
            
            if quote.patient.info.nationality:
                patient_info_data.append(['Nationality:', quote.patient.info.nationality])
            
            patient_table = Table(patient_info_data, colWidths=[1.8*inch, 4.7*inch])
            patient_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('TOPPADDING', (0, 0), (-1, -1), 3),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ]))
            
            story.append(patient_table)
            story.append(Spacer(1, 25))
        
        # Terms and Conditions
        story.append(Paragraph("TERMS & CONDITIONS", section_header_style))
        
        # Terms style
        terms_style = ParagraphStyle(
            'Terms',
            parent=styles['Normal'],
            fontSize=9,
            leading=12,
            spaceBefore=0,
            spaceAfter=0,
            leftIndent=0,
            rightIndent=0
        )
        
        terms_text = """
        • This quote is valid for 30 days from the date of issue<br/>
        • Payment is due upon acceptance of services<br/>
        • Cancellation policy: 24-hour notice required<br/>
        • Weather and operational delays may affect scheduling<br/>
        • All flights subject to FAA regulations and crew duty time requirements<br/>
        • Medical equipment and staff included as specified
        """
        
        story.append(Paragraph(terms_text, terms_style))
        story.append(Spacer(1, 25))
        
        # Footer
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.HexColor('#6B7280'),
            alignment=1,  # Center
            spaceBefore=0,
            spaceAfter=0,
            leading=10
        )
        
        story.append(Paragraph("Thank you for choosing JET ICU Medical Transport", footer_style))
        story.append(Paragraph("Your trusted partner in medical aviation", footer_style))
        
        # Build PDF
        doc.build(story)
        
        # Return PDF response
        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="quote_{quote.id.hex[:8]}.pdf"'
        return response
    
    @action(detail=True, methods=['post'])
    def generate_quote_document(self, request, pk=None):
        """
        Generate a Quote PDF document using the template and save it to nosign_out directory
        """
        import os
        from datetime import datetime
        from django.conf import settings
        from documents.templates.docs import populate_quote_pdf, QuoteData
        
        quote = self.get_object()
        
        try:
            # Prepare data for the quote document
            quote_data = QuoteData(
                quote_id=str(quote.id.hex[:8].upper()),
                inquiry_date=quote.inquiry_date.strftime('%Y-%m-%d') if quote.inquiry_date else '',
                patient_name=f"{quote.patient.info.first_name} {quote.patient.info.last_name}" if quote.patient and quote.patient.info else '',
                aircraft_type=dict(quote._meta.get_field('aircraft_type').choices).get(quote.aircraft_type, quote.aircraft_type),
                pickup_airport=f"{quote.pickup_airport.name} ({quote.pickup_airport.ident})" if quote.pickup_airport else '',
                dropoff_airport=f"{quote.dropoff_airport.name} ({quote.dropoff_airport.ident})" if quote.dropoff_airport else '',
                trip_date=quote.created_on.strftime('%Y-%m-%d') if quote.created_on else '',
                esitmated_flight_time=str(quote.estimated_flight_time) if quote.estimated_flight_time else '',
                number_of_stops=str(quote.number_of_stops),
                medical_team=dict(quote._meta.get_field('medical_team').choices).get(quote.medical_team, quote.medical_team),
                include_grounds='Yes' if quote.includes_grounds else 'No',
                our_availability='Available',
                amount=f"${quote.quoted_amount:,.2f}",
                notes=quote.notes if hasattr(quote, 'notes') else ''
            )
            
            # Define file paths
            template_path = os.path.join(settings.BASE_DIR, 'documents', 'templates', 'nosign_pdf', 'Quote.pdf')
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_filename = f"quote_{quote.id.hex[:8]}_{timestamp}.pdf"
            output_path = os.path.join(settings.BASE_DIR, 'documents', 'templates', 'nosign_out', output_filename)
            
            # Generate the PDF
            success = populate_quote_pdf(template_path, output_path, quote_data)
            
            if success:
                # Create Document record for tracking
                from .models import Document
                document = Document.objects.create(
                    filename=output_filename,
                    file_path=output_path,
                    document_type='quote',
                    created_by=request.user if request.user.is_authenticated else None
                )
                
                # Link document to trip that references this quote
                try:
                    trip = Trip.objects.get(quote_id=quote.id)
                    document.trip = trip
                    document.save()
                except Trip.DoesNotExist:
                    # No trip associated with this quote yet
                    pass
                
                return Response({
                    'success': True,
                    'message': 'Quote document generated successfully',
                    'filename': output_filename,
                    'path': output_path,
                    'document_id': str(document.id)
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'success': False,
                    'message': 'Failed to generate quote document'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error generating quote document: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'])
    def email(self, request, pk=None):
        """
        Email a quote with automatically generated PDF document and clean email content
        """
        from .serializers import EmailQuoteSerializer
        from utils.smtp.email import send_template
        from django.conf import settings
        import logging
        import os
        from datetime import datetime
        from documents.templates.docs import populate_quote_pdf, QuoteData

        logger = logging.getLogger(__name__)
        quote = self.get_object()

        # Validate request data
        serializer = EmailQuoteSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        email = data['email']
        subject = data['subject']
        message = data['message']

        try:
            # Generate quote document first (using existing logic)
            logger.info(f"Generating quote document for {quote.id}")

            # Prepare data for the quote document
            quote_data = QuoteData(
                quote_id=str(quote.id.hex[:8].upper()),
                inquiry_date=quote.inquiry_date.strftime('%Y-%m-%d') if quote.inquiry_date else '',
                patient_name=f"{quote.patient.info.first_name} {quote.patient.info.last_name}" if quote.patient and quote.patient.info else '',
                aircraft_type=str(quote.aircraft_type) if quote.aircraft_type else '',
                pickup_airport=f"{quote.pickup_airport.name} ({quote.pickup_airport.ident})" if quote.pickup_airport else '',
                dropoff_airport=f"{quote.dropoff_airport.name} ({quote.dropoff_airport.ident})" if quote.dropoff_airport else '',
                trip_date=quote.created_on.strftime('%Y-%m-%d') if quote.created_on else '',
                esitmated_flight_time=str(quote.estimated_flight_time) if quote.estimated_flight_time else '',
                number_of_stops=str(quote.number_of_stops),
                medical_team=quote.medical_team if quote.medical_team else '',
                include_grounds='Yes' if quote.includes_grounds else 'No',
                our_availability='Available',
                amount=f"${quote.quoted_amount:,.2f}" if quote.quoted_amount else '',
                notes=f"Quote generated on {datetime.now().strftime('%Y-%m-%d')}"
            )

            # Generate PDF and save as document
            template_base_path = os.path.join(settings.BASE_DIR, 'documents', 'templates', 'nosign_pdf')
            output_base_path = os.path.join(settings.BASE_DIR, 'documents', 'generated')
            os.makedirs(output_base_path, exist_ok=True)

            # Create unique filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_filename = f"quote_{quote.id.hex[:8]}_{timestamp}.pdf"
            input_path = os.path.join(template_base_path, 'Quote.pdf')
            output_path = os.path.join(output_base_path, output_filename)

            # Generate the PDF
            if populate_quote_pdf(input_path, output_path, quote_data):
                # Create Document record
                document = Document.objects.create(
                    filename=output_filename,
                    file_path=output_path,
                    document_type='quote',
                    created_by=request.user
                )

                # Get public download URL for document access (no authentication required)
                backend_url = getattr(settings, 'BACKEND_URL', 'http://localhost:8001')
                document_url = f"{backend_url}/api/documents/{document.id}/public_download/"

                # Build clean email content (without quote details)
                email_content = f"""
                {message}

                Please click the button below to view your quote document.

                Best regards,
                JET ICU Medical Transport Team
                Phone: (352) 796-2540
                Email: info@jeticu.com
                """

                # Send email with "Download Quote PDF" button
                success = send_template(
                    subject=subject,
                    targets=[email],
                    title=email_content,
                    link=document_url,
                    link_text="Download Quote PDF"
                )

                if success:
                    # Update quote with sent email info
                    quote.quote_pdf_email = email
                    quote.save()

                    logger.info(f"Quote #{str(quote.id)[:8]} with document emailed successfully to {email}")

                    return Response({
                        'success': True,
                        'message': f'Quote with PDF document emailed successfully to {email}',
                        'document_id': str(document.id),
                        'document_url': document_url
                    })
                else:
                    logger.error(f"Failed to send quote #{str(quote.id)[:8]} to {email}")
                    return Response({
                        'success': False,
                        'message': 'Failed to send email. Please check your email configuration.'
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            else:
                logger.error(f"Failed to generate quote document for {quote.id}")
                return Response({
                    'success': False,
                    'message': 'Failed to generate quote document'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            logger.error(f"Error emailing quote #{str(quote.id)[:8]}: {str(e)}")
            return Response({
                'success': False,
                'message': f'Error sending email: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Passenger ViewSet
class PassengerViewSet(BaseViewSet):
    queryset = Passenger.objects.select_related('info', 'passport_document')
    search_fields = ['info__first_name', 'info__last_name', 'nationality']
    ordering_fields = ['created_on']
    permission_classes = [
        permissions.IsAuthenticated,
        CanReadPassenger | CanWritePassenger | CanModifyPassenger | CanDeletePassenger
    ]
    
    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return PassengerReadSerializer
        return PassengerWriteSerializer
    
    def get_permissions(self):
        """
        Instantiate and return the list of permissions that this view requires.
        """
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [permissions.IsAuthenticated, CanReadPassenger]
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated, CanWritePassenger]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [permissions.IsAuthenticated, CanModifyPassenger]
        elif self.action == 'destroy':
            permission_classes = [permissions.IsAuthenticated, CanDeletePassenger]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

# CrewLine ViewSet
class CrewLineViewSet(BaseViewSet):
    queryset = CrewLine.objects.select_related('primary_in_command', 'secondary_in_command').prefetch_related('medic_ids')
    ordering_fields = ['created_on']
    
    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return CrewLineReadSerializer
        return CrewLineWriteSerializer

# Trip ViewSet
class TripViewSet(BaseViewSet):
    queryset = Trip.objects.select_related('quote', 'patient', 'patient__info', 'aircraft').prefetch_related('trip_lines', 'passengers__info', 'events__airport', 'events__crew_line')
    search_fields = ['trip_number', 'type', 'patient__info__first_name', 'patient__info__last_name', 'passengers__info__first_name', 'passengers__info__last_name']
    ordering_fields = ['created_on', 'estimated_departure_time']
    filterset_fields = ['status', 'type']  # Add filtering by status and type
    permission_classes = [
        permissions.IsAuthenticated,
        CanReadTrip | CanWriteTrip | CanModifyTrip | CanDeleteTrip
    ]
    
    def generate_trip_number(self):
        """
        Generate a unique five-digit auto-incrementing trip number.
        Format: 00001, 00002, etc.
        """
        from django.db.models import Max
        import re
        
        # Get the highest existing trip number
        max_trip = Trip.objects.aggregate(max_num=Max('trip_number'))['max_num']
        
        if not max_trip:
            # First trip
            return '00001'
        
        # Extract numeric value from trip numbers (handle various formats)
        try:
            # Try to extract numeric part from trip number
            match = re.search(r'\d+', max_trip)
            if match:
                max_num = int(match.group())
            else:
                max_num = 0
        except (ValueError, AttributeError):
            # If we can't parse existing numbers, start fresh
            max_num = 0
        
        # Increment and format as 5-digit number
        new_num = max_num + 1
        return str(new_num).zfill(5)
    
    def get_serializer_class(self):
        if self.action in ('list', 'retrieve', 'trip_lines'):
            return TripReadSerializer
        return TripWriteSerializer
    
    def perform_create(self, serializer):
        """
        Override perform_create to automatically generate trip number if not provided.
        """
        # Check if trip_number is provided in the validated data
        if not serializer.validated_data.get('trip_number'):
            # Generate a unique trip number
            trip_number = self.generate_trip_number()
            
            # Ensure uniqueness (in case of race conditions)
            while Trip.objects.filter(trip_number=trip_number).exists():
                # If somehow the number exists, generate the next one
                import re
                match = re.search(r'\d+', trip_number)
                if match:
                    num = int(match.group()) + 1
                    trip_number = str(num).zfill(5)
                else:
                    # Fallback to timestamp if we can't parse
                    import time
                    trip_number = f"T{int(time.time())}"
            
            # Save with the generated trip number
            instance = serializer.save(created_by=self.request.user, trip_number=trip_number)
        else:
            # Trip number was provided, use it
            instance = serializer.save(created_by=self.request.user)
        
        # Track creation
        from .utils import track_creation
        track_creation(instance, self.request.user)
    
    def get_permissions(self):
        """
        Instantiate and return the list of permissions that this view requires.
        """
        if self.action == 'list' or self.action == 'retrieve' or self.action == 'trip_lines':
            permission_classes = [permissions.IsAuthenticated, CanReadTrip]
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated, CanWriteTrip]
        elif self.action in ['update', 'partial_update', 'generate_itineraries', 'generate_handling_requests', 'generate_gen_dec']:
            permission_classes = [permissions.IsAuthenticated, CanModifyTrip]
        elif self.action == 'destroy':
            permission_classes = [permissions.IsAuthenticated, CanDeleteTrip]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @action(detail=True, methods=['post'])
    def generate_itineraries(self, request, pk=None):
        """
        Generate itinerary documents - one per crew line in the trip
        """
        import os
        from datetime import datetime
        from django.conf import settings
        from documents.templates.docs import populate_itinerary_pdf, ItineraryData, CrewInfo, FlightLeg, AirportInfo, TimeInfo
        
        trip = self.get_object()
        generated_files = []
        
        try:
            # Get all crew lines for this trip
            crew_lines = CrewLine.objects.filter(trip_lines__trip=trip).distinct()
            
            if not crew_lines.exists():
                return Response({
                    'success': False,
                    'message': 'No crew lines found for this trip'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            for crew_line in crew_lines:
                # Prepare crew info
                crew_info = CrewInfo(
                    pic=f"{crew_line.primary_in_command.first_name} {crew_line.primary_in_command.last_name}" if crew_line.primary_in_command else '',
                    sic=f"{crew_line.secondary_in_command.first_name} {crew_line.secondary_in_command.last_name}" if crew_line.secondary_in_command else ''
                )
                
                # Add medical crew members
                medics = list(crew_line.medic_ids.all())
                if len(medics) > 0:
                    crew_info.med_1 = f"{medics[0].first_name} {medics[0].last_name}"
                if len(medics) > 1:
                    crew_info.med_2 = f"{medics[1].first_name} {medics[1].last_name}"
                if len(medics) > 2:
                    crew_info.med_4 = f"{medics[2].first_name} {medics[2].last_name}"
                
                # Prepare flight legs
                flight_legs = []
                trip_lines = trip.trip_lines.filter(crew_line=crew_line).order_by('departure_time_utc')
                
                for i, trip_line in enumerate(trip_lines, 1):
                    leg = FlightLeg(
                        leg=str(i),
                        departure_id=trip_line.origin_airport.ident if trip_line.origin_airport else '',
                        edt_utc_local=trip_line.departure_time_local.strftime('%H:%M %Z') if trip_line.departure_time_local else '',
                        arrival_id=trip_line.destination_airport.ident if trip_line.destination_airport else '',
                        flight_time=str(trip_line.flight_time) if trip_line.flight_time else '',
                        eta_utc_local=trip_line.arrival_time_local.strftime('%H:%M %Z') if trip_line.arrival_time_local else '',
                        ground_time=str(trip_line.ground_time) if trip_line.ground_time else '',
                        pax_leg='Yes' if trip_line.passenger_leg else 'No'
                    )
                    flight_legs.append(leg)
                
                # Prepare airport info
                airports = []
                all_airports = set()
                for trip_line in trip_lines:
                    all_airports.add(trip_line.origin_airport)
                    all_airports.add(trip_line.destination_airport)
                
                for airport in all_airports:
                    if airport:
                        airport_info = AirportInfo(
                            icao=airport.icao_code or airport.ident,
                            airport_city_name=airport.name,
                            state_country=f"{airport.iso_region}, {airport.iso_country}",
                            time_zone=getattr(airport, 'timezone', ''),
                            fbo_handler='',  # Will be populated from FBO data if available
                            freq='',
                            phone_fax='',
                            fuel=''
                        )
                        airports.append(airport_info)
                
                # Prepare timing info
                times = TimeInfo(
                    showtime='',
                    origin_edt=trip.estimated_departure_time.strftime('%H:%M %Z') if trip.estimated_departure_time else '',
                    total_flight_time='',
                    total_duty_time='',
                    pre_flight_duty_time=str(trip.pre_flight_duty_time) if trip.pre_flight_duty_time else '',
                    post_flight_duty_time=str(trip.post_flight_duty_time) if trip.post_flight_duty_time else ''
                )
                
                # Prepare passenger list
                passengers = []
                for passenger in trip.passengers.all():
                    if passenger.info:
                        passengers.append(f"{passenger.info.first_name} {passenger.info.last_name}")
                
                # Create itinerary data
                itinerary_data = ItineraryData(
                    trip_number=trip.trip_number or '',
                    tail_number=trip.aircraft.tail_number if trip.aircraft else '',
                    trip_date=trip.trip_lines.first().departure_time_local.strftime('%Y-%m-%d') if trip.trip_lines.exists() and trip.trip_lines.first().departure_time_local else '',
                    trip_type=trip.type.title() if trip.type else 'Charter',
                    patient_name=f"{trip.patient.info.first_name} {trip.patient.info.last_name}" if trip.patient and trip.patient.info else '',
                    bed_at_origin=trip.patient.bed_at_origin if trip.patient else False,
                    bed_at_dest=trip.patient.bed_at_destination if trip.patient else False,
                    special_instructions=trip.patient.special_instructions if trip.patient else trip.notes or '',
                    passengers=passengers,
                    crew=crew_info,
                    flight_legs=flight_legs,
                    airports=airports,
                    times=times
                )
                
                # Define file paths
                template_path = os.path.join(settings.BASE_DIR, 'documents', 'templates', 'nosign_pdf', 'itin-2.pdf')
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                output_filename = f"itin_{trip.trip_number}_crew_{crew_line.id.hex[:8]}_{timestamp}.pdf"
                output_path = os.path.join(settings.BASE_DIR, 'documents', 'templates', 'nosign_out', output_filename)
                
                # Generate the PDF
                success = populate_itinerary_pdf(template_path, output_path, itinerary_data)
                
                if success:
                    # Create Document record for tracking
                    from .models import Document
                    document = Document.objects.create(
                        filename=output_filename,
                        file_path=output_path,
                        document_type='customer_itinerary',
                        trip=trip,
                        created_by=request.user if request.user.is_authenticated else None
                    )
                    
                    generated_files.append({
                        'crew_line_id': str(crew_line.id),
                        'filename': output_filename,
                        'path': output_path,
                        'document_id': str(document.id)
                    })
                else:
                    return Response({
                        'success': False,
                        'message': f'Failed to generate itinerary for crew line {crew_line.id}'
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            return Response({
                'success': True,
                'message': f'Generated {len(generated_files)} itinerary documents',
                'files': generated_files
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error generating itinerary documents: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['post'])
    def generate_handling_requests(self, request, pk=None):
        """
        Generate handling request documents - one per trip leg with FBO info from arriving airport
        """
        import os
        from datetime import datetime
        from django.conf import settings
        from documents.templates.docs import populate_handling_request_pdf, HandlingRequestData, PassengerInfo
        
        trip = self.get_object()
        generated_files = []
        
        try:
            # Get all trip lines for this trip
            trip_lines = trip.trip_lines.all().order_by('departure_time_utc')
            
            if not trip_lines.exists():
                return Response({
                    'success': False,
                    'message': 'No trip lines found for this trip'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            for trip_line in trip_lines:
                # Prepare aircraft data
                aircraft = trip.aircraft
                handling_data = HandlingRequestData(
                    company='JET Aviation Operations',
                    make=aircraft.make if aircraft else '',
                    model=aircraft.model if aircraft else '',
                    tail_number=aircraft.tail_number if aircraft else '',
                    serial_number=getattr(aircraft, 'serial_number', '') or '',
                    mgtow=str(getattr(aircraft, 'mgtow', '')) or '',
                    mission=trip.type.title() if trip.type else 'Charter',
                    depart_origin=trip_line.departure_time_local.strftime('%H:%M') if trip_line.departure_time_local else '',
                    arrive_dest=trip_line.arrival_time_local.strftime('%H:%M') if trip_line.arrival_time_local else '',
                    depart_dest='',  # For return legs - would need return trip line data
                    arrive_origin=''  # For return legs - would need return trip line data
                )
                
                # Prepare passenger information
                passengers = []
                for passenger in trip.passengers.all():
                    if passenger.info:
                        passenger_info = PassengerInfo(
                            name=f"{passenger.info.first_name} {passenger.info.last_name}",
                            title='',
                            nationality=getattr(passenger.info, 'nationality', '') or '',
                            date_of_birth=passenger.info.date_of_birth.strftime('%Y-%m-%d') if passenger.info.date_of_birth else '',
                            passport_number=getattr(passenger.info, 'passport_number', '') or '',
                            passport_expiration='',  # Would need passport expiration field
                            contact_number=passenger.info.phone or ''
                        )
                        passengers.append(passenger_info)
                
                # Add patient if exists and not already in passengers
                if trip.patient and trip.patient.info:
                    patient_already_added = any(
                        p.name == f"{trip.patient.info.first_name} {trip.patient.info.last_name}" 
                        for p in passengers
                    )
                    if not patient_already_added:
                        patient_info = PassengerInfo(
                            name=f"{trip.patient.info.first_name} {trip.patient.info.last_name}",
                            title='Patient',
                            nationality=getattr(trip.patient, 'nationality', ''),
                            date_of_birth=trip.patient.info.date_of_birth.strftime('%Y-%m-%d') if hasattr(trip.patient.info, 'date_of_birth') and trip.patient.info.date_of_birth else '',
                            passport_number='',
                            passport_expiration='',
                            contact_number=''
                        )
                        passengers.append(patient_info)
                
                handling_data.passengers = passengers
                
                # Define file paths
                template_path = os.path.join(settings.BASE_DIR, 'documents', 'templates', 'nosign_pdf', 'handling_request.pdf')
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                output_filename = f"handling_{trip.trip_number}_leg_{trip_line.id.hex[:8]}_{timestamp}.pdf"
                output_path = os.path.join(settings.BASE_DIR, 'documents', 'templates', 'nosign_out', output_filename)
                
                # Generate the PDF
                success = populate_handling_request_pdf(template_path, output_path, handling_data)
                
                if success:
                    # Create Document record for tracking
                    from .models import Document
                    document = Document.objects.create(
                        filename=output_filename,
                        file_path=output_path,
                        document_type='handling_request',
                        trip=trip,
                        created_by=request.user if request.user.is_authenticated else None
                    )
                    
                    generated_files.append({
                        'trip_line_id': str(trip_line.id),
                        'arrival_airport': trip_line.destination_airport.name if trip_line.destination_airport else '',
                        'arrival_fbo': trip_line.arrival_fbo.name if trip_line.arrival_fbo else 'N/A',
                        'filename': output_filename,
                        'path': output_path,
                        'document_id': str(document.id)
                    })
                else:
                    return Response({
                        'success': False,
                        'message': f'Failed to generate handling request for trip line {trip_line.id}'
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            return Response({
                'success': True,
                'message': f'Generated {len(generated_files)} handling request documents',
                'files': generated_files
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error generating handling request documents: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['post'])
    def generate_gen_dec(self, request, pk=None):
        """
        Generate general declaration documents for the trip with all current occupants
        Uses enhanced gen_dec.py module with proper member titles (PIC, SIC, MED, PAX)
        """
        import os
        from datetime import datetime
        from django.conf import settings
        from documents.templates.gen_dec import populate_gen_dec_pdf_enhanced, create_gen_dec_data_from_trip
        
        trip = self.get_object()
        
        try:
            # Check if trip has required data
            first_trip_line = trip.trip_lines.first()
            
            if not first_trip_line:
                return Response({
                    'success': False,
                    'message': 'No trip lines found for this trip'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Create enhanced gen dec data with proper member titles
            gen_dec_data = create_gen_dec_data_from_trip(trip)
            
            if gen_dec_data.total_occupants == 0:
                return Response({
                    'success': False,
                    'message': 'No occupants found for this trip'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Define file paths
            template_path = os.path.join(settings.BASE_DIR, 'documents', 'templates', 'nosign_pdf', 'gen_dec.pdf')
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_filename = f"gen_dec_{trip.trip_number}_{timestamp}.pdf"
            output_path = os.path.join(settings.BASE_DIR, 'documents', 'templates', 'nosign_out', output_filename)
            
            # Generate the PDF using enhanced function
            success = populate_gen_dec_pdf_enhanced(template_path, output_path, gen_dec_data)
            
            if success:
                # Create Document record for tracking
                from .models import Document
                document = Document.objects.create(
                    filename=output_filename,
                    file_path=output_path,
                    document_type='gendec',
                    trip=trip,
                    created_by=request.user if request.user.is_authenticated else None
                )
                
                # Create detailed occupant list with proper titles
                occupant_details = [str(member) for member in gen_dec_data.members]
                
                return Response({
                    'success': True,
                    'message': 'General declaration document generated successfully',
                    'file': {
                        'filename': output_filename,
                        'path': output_path,
                        'document_id': str(document.id),
                        'total_occupants': gen_dec_data.total_occupants,
                        'occupant_breakdown': {
                            'PIC': gen_dec_data.pic_count,
                            'SIC': gen_dec_data.sic_count,
                            'MED': gen_dec_data.med_count,
                            'PAX': gen_dec_data.pax_count
                        },
                        'occupant_details': occupant_details
                    }
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'success': False,
                    'message': 'Failed to generate general declaration document'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        except Exception as e:
            return Response({
                'success': False,
                'message': f'Error generating general declaration: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['get'])
    def trip_lines(self, request, pk=None):
        trip = self.get_object()
        trip_lines = trip.trip_lines.all().order_by('departure_time_utc')
        serializer = TripLineReadSerializer(trip_lines, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def timeline(self, request, pk=None):
        trip = self.get_object()
        legs = TripLineReadSerializer(trip.trip_lines.all(), many=True).data
        for item in legs:
            item["timeline_type"] = "LEG"
            item["sort_at"] = item["departure_time_utc"]

        events = TripEventReadSerializer(trip.events.all(), many=True).data
        for item in events:
            item["timeline_type"] = "EVENT"
            item["sort_at"] = item["start_time_utc"]

        combined = sorted(chain(legs, events), key=lambda x: x["sort_at"] or "")
        return Response(combined)

    @action(detail=False, methods=['get'])
    def live(self, request):
        """
        Get all trips that have live flights currently in progress.
        A flight is considered live if current time is between departure and arrival times.
        """
        now = timezone.now()

        # Find trips with trip lines where current time is between departure and arrival
        live_trips = Trip.objects.filter(
            trip_lines__departure_time_utc__lte=now,
            trip_lines__arrival_time_utc__gte=now,
            status='active'
        ).select_related(
            'aircraft', 'patient', 'patient__info'
        ).prefetch_related(
            'trip_lines__origin_airport',
            'trip_lines__destination_airport'
        ).distinct()

        live_flight_data = []

        for trip in live_trips:
            # Find the current active leg(s) for this trip
            active_legs = trip.trip_lines.filter(
                departure_time_utc__lte=now,
                arrival_time_utc__gte=now
            ).select_related('origin_airport', 'destination_airport')

            for leg in active_legs:
                # Calculate flight progress
                total_flight_time = leg.arrival_time_utc - leg.departure_time_utc
                elapsed_time = now - leg.departure_time_utc
                progress_percentage = (elapsed_time.total_seconds() / total_flight_time.total_seconds()) * 100

                # Determine flight phase
                if progress_percentage < 10:
                    phase = "departed"
                    phase_icon = "🛫"
                elif progress_percentage > 90:
                    phase = "approaching"
                    phase_icon = "🛬"
                else:
                    phase = "enroute"
                    phase_icon = "✈️"

                # Calculate estimated remaining time
                remaining_time = leg.arrival_time_utc - now

                live_flight_data.append({
                    'trip_id': trip.id,
                    'trip_number': trip.trip_number,
                    'aircraft_tail': trip.aircraft.tail_number if trip.aircraft else 'N/A',
                    'origin_airport': {
                        'ident': leg.origin_airport.ident,
                        'name': leg.origin_airport.name,
                    },
                    'destination_airport': {
                        'ident': leg.destination_airport.ident,
                        'name': leg.destination_airport.name,
                    },
                    'departure_time_local': leg.departure_time_local,
                    'arrival_time_local': leg.arrival_time_local,
                    'estimated_arrival_utc': leg.arrival_time_utc,
                    'phase': phase,
                    'phase_icon': phase_icon,
                    'progress_percentage': round(progress_percentage, 1),
                    'remaining_minutes': round(remaining_time.total_seconds() / 60),
                    'patient_name': f"{trip.patient.info.first_name} {trip.patient.info.last_name}" if trip.patient and trip.patient.info else None,
                    'trip_type': trip.type,
                })

        return Response({
            'live_flights': live_flight_data,
            'count': len(live_flight_data),
            'timestamp': now
        })

    @action(detail=True, methods=['post'])
    def generate_documents(self, request, pk=None):
        """
        Generate PDF documents for a trip using PDF templates.
        Accepts optional 'document_type' in request body to generate specific document.
        If no document_type provided, generates all applicable documents.
        """
        import os
        from datetime import datetime
        from django.conf import settings
        from documents.templates.docs import populate_quote_pdf, QuoteData, populate_itinerary_pdf, ItineraryData, CrewInfo, FlightLeg, AirportInfo, TimeInfo, populate_handling_request_pdf, HandlingRequestData, PassengerInfo
        from .serializers import DocumentSerializer, DocumentCreateSerializer
        
        trip = self.get_object()
        
        # Validate request data
        serializer = DocumentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        document_type = serializer.validated_data.get('document_type')
        
        try:
            generated_documents = []
            
            # Define base paths
            template_base_path = os.path.join(settings.BASE_DIR, 'documents', 'templates', 'nosign_pdf')
            output_base_path = os.path.join(settings.BASE_DIR, 'documents', 'generated')
            
            # Ensure output directory exists
            os.makedirs(output_base_path, exist_ok=True)
            
            # Available document generators
            document_generators = {
                'gendec': self._generate_gendec_pdf,
                'quote': self._generate_quote_pdf,
                'customer_itinerary': lambda trip, template_path, output_path: self._generate_itinerary_pdf(trip, template_path, output_path, 'customer_itinerary'),
                'internal_itinerary': lambda trip, template_path, output_path: self._generate_itinerary_pdf(trip, template_path, output_path, 'internal_itinerary'),
                'handling_request': self._generate_handling_request_pdf,
            }
            
            if document_type:
                # Generate specific document type
                if document_type in document_generators:
                    doc = document_generators[document_type](trip, template_base_path, output_base_path)
                    if doc:
                        generated_documents.append(doc)
                else:
                    return Response({
                        'error': f'Document type {document_type} not supported'
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                # Generate all applicable documents
                for doc_type in ['quote', 'customer_itinerary', 'handling_request', 'gendec', 'internal_itinerary']:
                    try:
                        doc = document_generators[doc_type](trip, template_base_path, output_base_path)
                        if doc:
                            generated_documents.append(doc)
                    except Exception as e:
                        print(f"Error generating {doc_type}: {e}")
                        continue
            
            return Response({
                'message': f'{len(generated_documents)} documents generated successfully',
                'documents': DocumentSerializer(generated_documents, many=True).data
            }, status=status.HTTP_201_CREATED)
                
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def _generate_quote_pdf(self, trip, template_base_path, output_base_path):
        """Generate quote PDF document"""
        try:
            import os
            from datetime import datetime
            import uuid
            
            # Create filename
            timestamp = datetime.now().strftime('%Y%m%d')
            unique_id = str(uuid.uuid4())[:8]
            filename = f"{trip.trip_number}-quote-{timestamp}-{unique_id}.pdf"
            
            # Input and output paths
            input_path = os.path.join(template_base_path, 'Quote.pdf')
            output_path = os.path.join(output_base_path, filename)
            
            if not os.path.exists(input_path):
                print(f"Quote template not found: {input_path}")
                return None
            
            # Prepare quote data
            from documents.templates.docs import QuoteData, populate_quote_pdf
            
            quote_data = QuoteData(
                quote_id=str(trip.quote.id) if trip.quote else '',
                inquiry_date=trip.quote.created_on.strftime('%Y-%m-%d') if trip.quote else '',
                patient_name=f"{trip.patient.info.first_name} {trip.patient.info.last_name}" if trip.patient and trip.patient.info else '',
                aircraft_type=trip.aircraft.make + ' ' + trip.aircraft.model if trip.aircraft else '',
                pickup_airport=trip.trip_lines.first().origin_airport.name if trip.trip_lines.exists() else '',
                dropoff_airport=trip.trip_lines.last().destination_airport.name if trip.trip_lines.exists() else '',
                trip_date=trip.trip_lines.first().departure_time_local.strftime('%Y-%m-%d') if trip.trip_lines.exists() and trip.trip_lines.first().departure_time_local else '',
                esitmated_flight_time=str(trip.quote.estimated_flight_time) if trip.quote and trip.quote.estimated_flight_time else '',
                medical_team=trip.quote.medical_team if trip.quote else '',
                amount=str(trip.quote.quoted_amount) if trip.quote and trip.quote.quoted_amount else '',
                notes=trip.notes or ''
            )
            
            # Generate PDF
            success = populate_quote_pdf(input_path, output_path, quote_data)
            
            if success:
                # Create document record
                document = Document.objects.create(
                    trip=trip,
                    document_type='quote',
                    filename=filename,
                    file_path=output_path,
                    created_by=self.request.user if hasattr(self.request, 'user') else None
                )
                return document
            return None
            
        except Exception as e:
            print(f"Error generating quote PDF: {e}")
            return None
    
    def _generate_itinerary_pdf(self, trip, template_base_path, output_base_path, doc_type='customer_itinerary'):
        """Generate itinerary PDF document"""
        try:
            import os
            from datetime import datetime
            import uuid
            
            # Create filename
            timestamp = datetime.now().strftime('%Y%m%d')
            unique_id = str(uuid.uuid4())[:8]
            filename = f"{trip.trip_number}-{doc_type.replace('_', '_')}-{timestamp}-{unique_id}.pdf"
            
            # Input and output paths
            input_path = os.path.join(template_base_path, 'itin.pdf')
            output_path = os.path.join(output_base_path, filename)
            
            if not os.path.exists(input_path):
                print(f"Itinerary template not found: {input_path}")
                return None
            
            # Prepare itinerary data
            from documents.templates.docs import ItineraryData, CrewInfo, FlightLeg, AirportInfo, TimeInfo, populate_itinerary_pdf
            
            # Create crew info
            crew_lines = CrewLine.objects.filter(trip_lines__trip=trip).distinct()
            crew_info = CrewInfo()
            if crew_lines.exists():
                crew_line = crew_lines.first()
                if crew_line.primary_in_command:
                    crew_info.pic = f"{crew_line.primary_in_command.first_name} {crew_line.primary_in_command.last_name}"
                if crew_line.secondary_in_command:
                    crew_info.sic = f"{crew_line.secondary_in_command.first_name} {crew_line.secondary_in_command.last_name}"
            
            # Create flight legs
            flight_legs = []
            for i, trip_line in enumerate(trip.trip_lines.all(), 1):
                leg = FlightLeg(
                    leg=str(i),
                    departure_id=trip_line.origin_airport.ident if trip_line.origin_airport else '',
                    arrival_id=trip_line.destination_airport.ident if trip_line.destination_airport else '',
                    flight_time=str(trip_line.flight_time) if trip_line.flight_time else '',
                    pax_leg='Yes' if trip_line.passenger_leg else 'No'
                )
                flight_legs.append(leg)
            
            # Prepare passenger list
            passengers = []
            for passenger in trip.passengers.all():
                if passenger.info:
                    passengers.append(f"{passenger.info.first_name} {passenger.info.last_name}")
            
            itinerary_data = ItineraryData(
                trip_number=trip.trip_number or '',
                patient_name=f"{trip.patient.info.first_name} {trip.patient.info.last_name}" if trip.patient and trip.patient.info else '',
                passengers=passengers,
                crew=crew_info,
                flight_legs=flight_legs
            )
            
            # Generate PDF
            success = populate_itinerary_pdf(input_path, output_path, itinerary_data)
            
            if success:
                # Create document record
                document = Document.objects.create(
                    trip=trip,
                    document_type=doc_type,
                    filename=filename,
                    file_path=output_path,
                    created_by=self.request.user if hasattr(self.request, 'user') else None
                )
                return document
            return None
            
        except Exception as e:
            print(f"Error generating itinerary PDF: {e}")
            return None
    
    def _generate_handling_request_pdf(self, trip, template_base_path, output_base_path):
        """Generate handling request PDF document"""
        try:
            import os
            from datetime import datetime
            import uuid
            
            # Create filename
            timestamp = datetime.now().strftime('%Y%m%d')
            unique_id = str(uuid.uuid4())[:8]
            filename = f"{trip.trip_number}-handling_request-{timestamp}-{unique_id}.pdf"
            
            # Input and output paths
            input_path = os.path.join(template_base_path, 'handling_request.pdf')
            output_path = os.path.join(output_base_path, filename)
            
            if not os.path.exists(input_path):
                print(f"Handling request template not found: {input_path}")
                return None
            
            # Prepare handling request data
            from documents.templates.docs import HandlingRequestData, PassengerInfo, populate_handling_request_pdf
            
            # Prepare passenger info
            passengers = []
            for passenger in trip.passengers.all():
                if passenger.info:
                    pax_info = PassengerInfo(
                        name=f"{passenger.info.first_name} {passenger.info.last_name}",
                        nationality=passenger.info.nationality or '',
                        date_of_birth=passenger.info.date_of_birth.strftime('%Y-%m-%d') if passenger.info.date_of_birth else '',
                        passport_number=passenger.info.passport_number or '',
                        passport_expiration=passenger.info.passport_expiration_date.strftime('%Y-%m-%d') if passenger.info.passport_expiration_date else '',
                        contact_number=passenger.info.phone or ''
                    )
                    passengers.append(pax_info)
            
            handling_data = HandlingRequestData(
                company=trip.aircraft.company if trip.aircraft else 'JET ICU Medical Transport',
                make=trip.aircraft.make if trip.aircraft else '',
                model=trip.aircraft.model if trip.aircraft else '',
                tail_number=trip.aircraft.tail_number if trip.aircraft else '',
                serial_number=trip.aircraft.serial_number if trip.aircraft else '',
                mgtow=str(trip.aircraft.mgtow) if trip.aircraft and trip.aircraft.mgtow else '',
                passengers=passengers
            )
            
            # Generate PDF
            success = populate_handling_request_pdf(input_path, output_path, handling_data)
            
            if success:
                # Create document record
                document = Document.objects.create(
                    trip=trip,
                    document_type='handling_request',
                    filename=filename,
                    file_path=output_path,
                    created_by=self.request.user if hasattr(self.request, 'user') else None
                )
                return document
            return None
            
        except Exception as e:
            print(f"Error generating handling request PDF: {e}")
            return None
    
    def _generate_gendec_pdf(self, trip, template_base_path, output_base_path):
        """Generate general declaration document - placeholder for now"""
        try:
            # For now, return None since there's no gendec PDF template
            # The system seems to be generating DOCX files via a different system
            print("gendec generation not implemented for PDF system - using DOCX templating system")
            return None
            
        except Exception as e:
            print(f"Error generating gendec PDF: {e}")
            return None
    
    @action(detail=True, methods=['get'])
    def documents(self, request, pk=None):
        """
        List all documents associated with a trip.
        """
        from .serializers import DocumentSerializer
        
        trip = self.get_object()
        documents = trip.documents.all().order_by('-created_on')
        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data)

# Document ViewSet
class DocumentViewSet(BaseViewSet):
    queryset = Document.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        from .serializers import DocumentSerializer
        return DocumentSerializer
    
    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """
        Download a document file.
        """
        from django.http import FileResponse
        from pathlib import Path
        
        document = self.get_object()
        
        if document.file_path and Path(document.file_path).exists():
            file_path = Path(document.file_path)
            response = FileResponse(
                open(file_path, 'rb'),
                content_type='application/octet-stream'
            )
            response['Content-Disposition'] = f'attachment; filename="{document.filename}"'
            return response
        elif document.content:
            # Fallback to binary content if stored in database
            response = HttpResponse(document.content, content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{document.filename}"'
            return response
        else:
            return Response(
                {'error': 'Document file not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['get'], permission_classes=[])
    def public_download(self, request, pk=None):
        """
        Public download endpoint for documents that doesn't require authentication.
        Used for email links to quote PDFs and other documents.
        """
        from django.http import FileResponse, HttpResponse
        from pathlib import Path

        document = self.get_object()

        # Only allow public download for certain document types (like quotes)
        allowed_types = ['quote', 'customer_itinerary', 'gendec', 'handling_request']
        if document.document_type not in allowed_types:
            return Response(
                {'error': 'This document type is not available for public download'},
                status=status.HTTP_403_FORBIDDEN
            )

        if document.file_path and Path(document.file_path).exists():
            file_path = Path(document.file_path)
            response = FileResponse(
                open(file_path, 'rb'),
                content_type='application/pdf'
            )
            response['Content-Disposition'] = f'attachment; filename="{document.filename}"'
            return response
        elif document.content:
            # Fallback to binary content if stored in database
            response = HttpResponse(document.content, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{document.filename}"'
            return response
        else:
            return Response(
                {'error': 'Document file not found'},
                status=status.HTTP_404_NOT_FOUND
            )

# TripLine ViewSet
class TripLineViewSet(BaseViewSet):
    queryset = TripLine.objects.select_related('trip', 'origin_airport', 'destination_airport', 'crew_line')
    ordering_fields = ['departure_time_utc', 'created_on']
    permission_classes = [
        permissions.IsAuthenticated,
        CanReadTripLine | CanWriteTripLine | CanModifyTripLine | CanDeleteTripLine
    ]
    
    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TripLineReadSerializer
        return TripLineWriteSerializer
    
    def get_permissions(self):
        """
        Instantiate and return the list of permissions that this view requires.
        """
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [permissions.IsAuthenticated, CanReadTripLine]
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated, CanWriteTripLine]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [permissions.IsAuthenticated, CanModifyTripLine]
        elif self.action == 'destroy':
            permission_classes = [permissions.IsAuthenticated, CanDeleteTripLine]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        trip_line = serializer.save(created_by=self.request.user)
        trip = trip_line.trip
        
        # Recalculate times for all trip lines in this trip
        if trip.estimated_departure_time:
            self.recalculate_trip_times(trip)
    
    def perform_update(self, serializer):
        trip_line = serializer.save()
        trip = trip_line.trip
        
        # Recalculate times for all trip lines in this trip
        if trip.estimated_departure_time:
            self.recalculate_trip_times(trip)
    
    def recalculate_trip_times(self, trip):
        # This is a placeholder for the actual time calculation logic
        # In a real implementation, this would update all trip lines based on
        # the trip's estimated departure time and the flight/ground times of each leg
        pass

# Modification ViewSet for tracking changes
class ModificationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Modification.objects.all()
    serializer_class = ModificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['model', 'field']
    ordering_fields = ['time']
    
    @action(detail=False, methods=['get'])
    def for_object(self, request):
        model = request.query_params.get('model')
        object_id = request.query_params.get('object_id')
        
        if not model or not object_id:
            return Response({"detail": "Missing parameters"}, status=status.HTTP_400_BAD_REQUEST)
            
        modifications = Modification.objects.filter(
            model=model,
            object_id=object_id
        ).order_by('-time')
        
        serializer = self.get_serializer(modifications, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    """
    Get dashboard statistics for JET ICU Operations
    """
    from django.db.models import Count, Sum, Q
    from datetime import datetime, timedelta
    from django.utils import timezone
    
    now = timezone.now()
    thirty_days_ago = now - timedelta(days=30)
    
    # Trip statistics
    total_trips = Trip.objects.count()
    active_trips = Trip.objects.filter(
        Q(estimated_departure_time__gte=now) | 
        Q(estimated_departure_time__isnull=True)
    ).exclude(status='completed').count()
    
    completed_trips_30_days = Trip.objects.filter(
        status='completed',
        created_on__gte=thirty_days_ago
    ).count()
    
    # Quote statistics
    total_quotes = Quote.objects.count()
    pending_quotes = Quote.objects.filter(status='pending').count()
    active_quotes = Quote.objects.filter(status='active').count()
    completed_quotes = Quote.objects.filter(status='completed').count()
    
    # Patient statistics
    total_patients = Patient.objects.count()
    active_patients = Patient.objects.filter(status__in=['confirmed', 'active']).count()
    
    # Aircraft statistics
    total_aircraft = Aircraft.objects.count()
    
    # Financial statistics
    total_revenue = Quote.objects.filter(
        status__in=['completed', 'paid']
    ).aggregate(Sum('quoted_amount'))['quoted_amount__sum'] or 0
    
    pending_revenue = Quote.objects.filter(
        status='active'
    ).aggregate(Sum('quoted_amount'))['quoted_amount__sum'] or 0
    
    # Recent activity
    recent_quotes = Quote.objects.filter(
        created_on__gte=thirty_days_ago
    ).order_by('-created_on')[:5]
    
    recent_trips = Trip.objects.filter(
        created_on__gte=thirty_days_ago
    ).order_by('-created_on')[:5]
    
    # Trip types breakdown
    trip_types = Trip.objects.values('type').annotate(count=Count('type'))
    
    # Status breakdown for quotes
    quote_statuses = Quote.objects.values('status').annotate(count=Count('status'))
    
    return Response({
        'trip_stats': {
            'total': total_trips,
            'active': active_trips,
            'completed_30_days': completed_trips_30_days,
            'types_breakdown': list(trip_types)
        },
        'quote_stats': {
            'total': total_quotes,
            'pending': pending_quotes,
            'active': active_quotes,
            'completed': completed_quotes,
            'statuses_breakdown': list(quote_statuses)
        },
        'patient_stats': {
            'total': total_patients,
            'active': active_patients
        },
        'aircraft_stats': {
            'total': total_aircraft
        },
        'financial_stats': {
            'total_revenue': float(total_revenue),
            'pending_revenue': float(pending_revenue)
        },
        'recent_activity': {
            'quotes': [
                {
                    'id': str(q.id),
                    'amount': float(q.quoted_amount),
                    'status': q.status,
                    'created_on': q.created_on,
                    'patient_name': f"{q.patient.info.first_name or ''} {q.patient.info.last_name or ''}".strip() if q.patient and q.patient.info else 'No patient'
                } for q in recent_quotes
            ],
            'trips': [
                {
                    'id': str(t.id),
                    'trip_number': t.trip_number,
                    'type': t.type,
                    'status': t.status,
                    'created_on': t.created_on,
                    'estimated_departure': t.estimated_departure_time
                } for t in recent_trips
            ]
        }
    })


class StaffViewSet(BaseViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Staff.objects.select_related("contact").all().order_by("-created_on")
    search_fields = ['contact__first_name', 'contact__last_name', 'contact__business_name', 'contact__email']

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return StaffReadSerializer
        return StaffWriteSerializer


class StaffRoleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = StaffRole.objects.all().order_by("code")
    serializer_class = StaffRoleSerializer
    
    def perform_create(self, serializer):
        instance = serializer.save(created_by=self.request.user)
        track_creation(instance, self.request.user)
    
    def perform_update(self, serializer):
        instance = serializer.save(modified_by=self.request.user)
        # Updates are automatically tracked by signals
        
    def perform_destroy(self, instance):
        track_deletion(instance, self.request.user)
        instance.delete()

class LostReasonViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = LostReason.objects.filter(is_active=True).order_by("reason")
    serializer_class = LostReasonSerializer
    
    def perform_create(self, serializer):
        instance = serializer.save(created_by=self.request.user)
        track_creation(instance, self.request.user)
    
    def perform_update(self, serializer):
        instance = serializer.save(modified_by=self.request.user)
        # Updates are automatically tracked by signals
        
    def perform_destroy(self, instance):
        # Soft delete - just mark as inactive
        instance.is_active = False
        instance.save()
        track_deletion(instance, self.request.user)


class StaffRoleMembershipViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = StaffRoleMembership.objects.select_related("staff", "role").all().order_by("-created_on")

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filter by staff_id if provided
        staff_id = self.request.query_params.get('staff_id', None)
        if staff_id is not None:
            queryset = queryset.filter(staff_id=staff_id)
        return queryset

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return StaffRoleMembershipReadSerializer
        return StaffRoleMembershipWriteSerializer
    
    def perform_create(self, serializer):
        instance = serializer.save(created_by=self.request.user)
        track_creation(instance, self.request.user)
    
    def perform_update(self, serializer):
        instance = serializer.save(modified_by=self.request.user)
        # Updates are automatically tracked by signals
        
    def perform_destroy(self, instance):
        track_deletion(instance, self.request.user)
        instance.delete()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_contact_with_related(request):
    """
    Unified endpoint for creating contacts with related records (Patient, Staff, Passenger, Customer)
    
    POST /api/contacts/create-with-related/
    
    Body:
    {
        "first_name": "John",
        "last_name": "Doe", 
        "email": "john.doe@example.com",
        "phone": "+1234567890",
        "date_of_birth": "1990-01-01",
        "passport_number": "123456789",
        "passport_expiration_date": "2030-01-01",
        "nationality": "US",
        "related_type": "patient",  // "patient", "staff", "passenger", "customer"
        "related_data": {
            "special_instructions": "Requires wheelchair assistance",
            "bed_at_origin": true,
            "status": "confirmed"
        }
    }
    """
    serializer = ContactCreationSerializer(data=request.data, context={'request': request})
    
    if serializer.is_valid():
        try:
            result = serializer.save()
            
            # Return appropriate response based on related type
            contact = result['contact']
            related_instance = result['related_instance']
            related_type = result['related_type']
            
            response_data = {
                'contact': ContactReadSerializer(contact).data,
                'related_type': related_type,
                'success': True,
                'message': f'{related_type.capitalize()} created successfully'
            }
            
            # Add specific related data
            if related_type == 'patient':
                from .serializers import PatientReadSerializer
                response_data['patient'] = PatientReadSerializer(related_instance).data
            elif related_type == 'staff':
                response_data['staff'] = StaffReadSerializer(related_instance).data
            elif related_type == 'passenger':
                from .serializers import PassengerReadSerializer
                response_data['passenger'] = PassengerReadSerializer(related_instance).data
            elif related_type == 'customer':
                response_data['customer'] = ContactReadSerializer(related_instance).data
            
            return Response(response_data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                'error': str(e),
                'success': False
            }, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class TripEventViewSet(BaseViewSet):
    queryset = TripEvent.objects.select_related("trip", "airport", "crew_line")
    ordering_fields = ["start_time_utc", "created_on"]

    def get_serializer_class(self):
        return (TripEventReadSerializer
                if self.action in ("list", "retrieve")
                else TripEventWriteSerializer)


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing comments on any model instance.
    Supports filtering by content_type and object_id.
    """
    queryset = Comment.objects.select_related('created_by', 'content_type').order_by('-created_on')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['text']
    ordering_fields = ['created_on', 'modified_on']
    pagination_class = StandardPagination
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by content_type and object_id if provided
        content_type = self.request.query_params.get('content_type')
        object_id = self.request.query_params.get('object_id')
        
        if content_type:
            # Support both model name and content_type id
            if content_type.isdigit():
                queryset = queryset.filter(content_type_id=content_type)
            else:
                from django.contrib.contenttypes.models import ContentType
                try:
                    ct = ContentType.objects.get(model=content_type.lower())
                    queryset = queryset.filter(content_type=ct)
                except ContentType.DoesNotExist:
                    queryset = queryset.none()
        
        if object_id:
            queryset = queryset.filter(object_id=object_id)
        
        return queryset
    
    def perform_create(self, serializer):
        instance = serializer.save(created_by=self.request.user, modified_by=self.request.user)
        # Track creation
        track_creation(instance, self.request.user)
    
    def perform_update(self, serializer):
        instance = serializer.save(modified_by=self.request.user)
        # Updates are automatically tracked by signals
        
    def perform_destroy(self, instance):
        # Track deletion before destroying
        track_deletion(instance, self.request.user)
        instance.delete()
    
    @action(detail=False, methods=['get'])
    def for_object(self, request):
        """Get all comments for a specific object"""
        model_name = request.query_params.get('model')
        object_id = request.query_params.get('object_id')
        
        if not model_name or not object_id:
            return Response(
                {'error': 'Both model and object_id parameters are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        from django.contrib.contenttypes.models import ContentType
        try:
            content_type = ContentType.objects.get(model=model_name.lower())
            comments = self.get_queryset().filter(
                content_type=content_type,
                object_id=object_id
            )
            serializer = self.get_serializer(comments, many=True)
            return Response(serializer.data)
        except ContentType.DoesNotExist:
            return Response(
                {'error': f'Model {model_name} not found'},
                status=status.HTTP_404_NOT_FOUND
            )


# Timezone utility API endpoints
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_airport_timezone_info(request, airport_id):
    """
    Get timezone information for a specific airport at a given datetime
    Query params: datetime (ISO format, optional - defaults to current time)
    """
    try:
        from .models import Airport
        from .timezone_utils import get_timezone_info
        from datetime import datetime
        import pytz
        
        airport = Airport.objects.get(id=airport_id)
        
        if not airport.timezone:
            return Response({
                'error': 'Airport does not have timezone information'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Parse datetime from query params or use current time
        dt_param = request.query_params.get('datetime')
        if dt_param:
            try:
                dt = datetime.fromisoformat(dt_param.replace('Z', '+00:00'))
            except ValueError:
                return Response({
                    'error': 'Invalid datetime format. Use ISO format (e.g., 2023-12-25T14:30:00Z)'
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            from django.utils import timezone as django_timezone
            dt = django_timezone.now()
        
        tz_info = get_timezone_info(airport.timezone, dt)
        tz_info['airport'] = {
            'id': airport.id,
            'name': airport.name,
            'ident': airport.ident,
            'timezone': airport.timezone
        }
        
        return Response(tz_info)
        
    except Airport.DoesNotExist:
        return Response({
            'error': 'Airport not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'error': f'Error getting timezone info: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def validate_flight_times(request):
    """
    Validate timezone consistency between local and UTC times for flight legs
    
    Request body:
    {
        "departure_airport_id": "uuid",
        "departure_local": "2023-12-25T14:30:00",
        "departure_utc": "2023-12-25T19:30:00Z",
        "arrival_airport_id": "uuid", 
        "arrival_local": "2023-12-25T16:30:00",
        "arrival_utc": "2023-12-25T21:30:00Z"
    }
    """
    try:
        from .models import Airport
        from .timezone_utils import validate_time_consistency, check_dst_transition_warning, calculate_flight_duration_with_timezones
        from datetime import datetime
        
        data = request.data
        
        # Parse departure info
        dep_airport_id = data.get('departure_airport_id')
        dep_local_str = data.get('departure_local')
        dep_utc_str = data.get('departure_utc')
        
        # Parse arrival info
        arr_airport_id = data.get('arrival_airport_id')
        arr_local_str = data.get('arrival_local')
        arr_utc_str = data.get('arrival_utc')
        
        if not all([dep_airport_id, dep_local_str, dep_utc_str]):
            return Response({
                'error': 'departure_airport_id, departure_local, and departure_utc are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        dep_airport = Airport.objects.get(id=dep_airport_id)
        
        # Parse departure times
        dep_local = datetime.fromisoformat(dep_local_str.replace('Z', '+00:00')).replace(tzinfo=None)
        dep_utc = datetime.fromisoformat(dep_utc_str.replace('Z', '+00:00'))
        
        results = {
            'departure_valid': False,
            'arrival_valid': False,
            'warnings': []
        }
        
        # Validate departure times
        if dep_airport.timezone:
            results['departure_valid'] = validate_time_consistency(dep_local, dep_utc, dep_airport.timezone)
            
            # Check for DST warnings
            dst_warning = check_dst_transition_warning(dep_local, dep_airport.timezone)
            if dst_warning:
                results['warnings'].append(f"Departure: {dst_warning['message']}")
        
        # Validate arrival times if provided
        if arr_airport_id and arr_local_str and arr_utc_str:
            arr_airport = Airport.objects.get(id=arr_airport_id)
            arr_local = datetime.fromisoformat(arr_local_str.replace('Z', '+00:00')).replace(tzinfo=None)
            arr_utc = datetime.fromisoformat(arr_utc_str.replace('Z', '+00:00'))
            
            if arr_airport.timezone:
                results['arrival_valid'] = validate_time_consistency(arr_local, arr_utc, arr_airport.timezone)
                
                # Check for DST warnings
                dst_warning = check_dst_transition_warning(arr_local, arr_airport.timezone)
                if dst_warning:
                    results['warnings'].append(f"Arrival: {dst_warning['message']}")
                
                # Calculate flight duration with timezone info
                duration, info = calculate_flight_duration_with_timezones(
                    dep_local, dep_airport.timezone,
                    arr_local, arr_airport.timezone
                )
                
                results['flight_duration_hours'] = duration
                results['flight_info'] = info
        
        results['overall_valid'] = results['departure_valid'] and (
            results['arrival_valid'] if 'arrival_valid' in results and arr_airport_id else True
        )
        
        return Response(results)
        
    except Airport.DoesNotExist:
        return Response({
            'error': 'Airport not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'error': f'Validation error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def convert_timezone(request):
    """
    Convert departure time + flight duration to arrival time accounting for timezones
    Used by frontend forms to display correct arrival times
    """
    try:
        departure_date = request.data.get('departure_date')
        departure_time = request.data.get('departure_time')
        flight_time_hours = request.data.get('flight_time_hours')
        origin_timezone = request.data.get('origin_timezone')
        destination_timezone = request.data.get('destination_timezone')
        
        if not all([departure_date, departure_time, flight_time_hours, origin_timezone, destination_timezone]):
            return Response({
                'error': 'Missing required fields: departure_date, departure_time, flight_time_hours, origin_timezone, destination_timezone'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        from .timezone_utils import convert_local_to_utc, convert_utc_to_local
        from datetime import datetime, timedelta
        
        # Create departure datetime
        departure_local = datetime.strptime(f"{departure_date} {departure_time}:00", "%Y-%m-%d %H:%M:%S")
        
        # Convert to UTC using origin timezone
        departure_utc = convert_local_to_utc(departure_local, origin_timezone)
        
        # Add flight time
        arrival_utc = departure_utc + timedelta(hours=float(flight_time_hours))
        
        # Convert to destination local time
        arrival_local = convert_utc_to_local(arrival_utc, destination_timezone)
        
        return Response({
            'arrival_date': arrival_local.date().isoformat(),
            'arrival_time': arrival_local.time().strftime('%H:%M'),
            'departure_utc': departure_utc.isoformat(),
            'arrival_utc': arrival_utc.isoformat(),
            'flight_duration_hours': float(flight_time_hours)
        })
        
    except Exception as e:
        return Response({
            'error': f'Timezone conversion error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Contract ViewSet
class ContractViewSet(BaseViewSet):
    queryset = Contract.objects.all()
    search_fields = ['title', 'contract_type', 'signer_email', 'status']
    ordering_fields = ['created_on', 'date_sent', 'date_signed', 'status']
    filterset_fields = ['contract_type', 'status', 'trip']
    
    def get_queryset(self):
        """Override to add custom filtering for trip parameter."""
        queryset = super().get_queryset()
        
        # Handle both DRF Request objects and regular Django requests
        if hasattr(self.request, 'query_params'):
            params = self.request.query_params
        else:
            params = self.request.GET
        
        # Filter by trip if provided
        trip_id = params.get('trip', None)
        if trip_id:
            queryset = queryset.filter(trip_id=trip_id)
            
        # Filter by contract type if provided
        contract_type = params.get('contract_type', None)
        if contract_type:
            queryset = queryset.filter(contract_type=contract_type)
            
        # Filter by status if provided
        status_filter = params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
            
        return queryset
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action in ['list', 'retrieve']:
            return ContractReadSerializer
        elif self.action == 'create_from_trip':
            return ContractCreateFromTripSerializer
        elif self.action in ['send_for_signature', 'docuseal_action']:
            return ContractDocuSealActionSerializer
        return ContractWriteSerializer
    
    @action(detail=False, methods=['post'])
    def create_from_trip(self, request):
        """Create multiple contracts for a trip."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        trip = serializer.validated_data['trip_id']
        contract_types = serializer.validated_data['contract_types']
        send_immediately = serializer.validated_data.get('send_immediately', False)
        custom_signer_email = serializer.validated_data.get('custom_signer_email')
        custom_signer_name = serializer.validated_data.get('custom_signer_name')
        manual_price = serializer.validated_data.get('manual_price')
        manual_price_description = serializer.validated_data.get('manual_price_description')
        
        try:
            # Get customer contact from quote
            customer_contact = None
            if trip.quote and hasattr(trip.quote, 'contact'):
                customer_contact = trip.quote.contact
            
            logger.info(f"Trip {trip.trip_number}: quote={bool(trip.quote)}, customer_contact={bool(customer_contact)}")
            patient = trip.patient
            
            # Determine signer details with fallback logic
            if custom_signer_email:
                signer_email = custom_signer_email
                signer_name = custom_signer_name or ''
            elif customer_contact:
                # Primary: Use quote's customer contact
                signer_email = customer_contact.email
                signer_name = f"{customer_contact.first_name} {customer_contact.last_name}".strip()
            elif patient and patient.info:
                # Fallback: Use patient contact info
                signer_email = patient.info.email
                signer_name = f"{patient.info.first_name} {patient.info.last_name}".strip()
                logger.info(f"Using patient as signer for trip {trip.trip_number}")
            else:
                # Check if payment agreement is requested without pricing info
                if 'payment_agreement' in contract_types and not trip.quote:
                    return Response({
                        'error': 'Payment agreement requires a quote with pricing information, or provide custom_signer_email and manual pricing'
                    }, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({
                        'error': 'No signer information available. Please provide custom_signer_email or ensure trip has a quote with customer contact or patient with contact info.'
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            contracts_created = []
            docuseal_service = DocuSealService()
            
            for contract_type in contract_types:
                # Generate contract title
                contract_type_display = dict(Contract.CONTRACT_TYPES)[contract_type]
                title = f"{contract_type_display} - {trip.trip_number}"
                
                # Create contract
                contract = Contract.objects.create(
                    title=title,
                    contract_type=contract_type,
                    trip=trip,
                    customer_contact=customer_contact,
                    patient=patient,
                    signer_email=signer_email,
                    signer_name=signer_name,
                    created_by=request.user
                )
                
                contracts_created.append(contract)
                
                # If send_immediately is True, attempt to send via DocuSeal
                if send_immediately:
                    try:
                        logger.info(f"Attempting to send contract {contract.id} for signature")
                        result = self._send_contract_for_signature(contract, docuseal_service, manual_price, manual_price_description)
                        logger.info(f"Successfully sent contract {contract.id}: {result}")
                    except Exception as e:
                        logger.error(f"Failed to send contract {contract.id}: {str(e)}", exc_info=True)
                        contract.status = 'failed'
                        contract.notes = f"Failed to send: {str(e)}"
                        contract.save()
            
            # Serialize created contracts
            serializer = ContractReadSerializer(contracts_created, many=True)
            
            return Response({
                'message': f'Created {len(contracts_created)} contracts',
                'contracts': serializer.data
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            logger.error(f"Failed to create contracts: {str(e)}")
            return Response({
                'error': f'Failed to create contracts: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['post'])
    def send_for_signature(self, request, pk=None):
        """Send contract to DocuSeal for signature."""
        contract = self.get_object()
        
        try:
            docuseal_service = DocuSealService()
            result = self._send_contract_for_signature(contract, docuseal_service)
            
            serializer = ContractReadSerializer(contract)
            return Response({
                'message': 'Contract sent for signature',
                'contract': serializer.data,
                'docuseal_response': result
            })
            
        except Exception as e:
            logger.error(f"Failed to send contract for signature: {str(e)}")
            return Response({
                'error': f'Failed to send contract: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['post'])
    def docuseal_action(self, request, pk=None):
        """Perform DocuSeal-specific actions on contract."""
        contract = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        action_type = serializer.validated_data['action']
        custom_message = serializer.validated_data.get('custom_message', '')
        
        try:
            docuseal_service = DocuSealService()
            
            if action_type == 'send_for_signature':
                result = self._send_contract_for_signature(contract, docuseal_service)
                message = 'Contract sent for signature'
                
            elif action_type == 'resend':
                result = self._resend_contract(contract, docuseal_service)
                message = 'Contract resent'
                
            elif action_type == 'cancel':
                result = self._cancel_contract(contract, docuseal_service)
                message = 'Contract cancelled'
                
            elif action_type == 'archive':
                result = self._archive_contract(contract, docuseal_service)
                message = 'Contract archived'
                
            else:
                return Response({
                    'error': f'Unknown action: {action_type}'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            contract_serializer = ContractReadSerializer(contract)
            return Response({
                'message': message,
                'contract': contract_serializer.data,
                'docuseal_response': result
            })
            
        except Exception as e:
            logger.error(f"DocuSeal action failed: {str(e)}")
            return Response({
                'error': f'Action failed: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def _send_contract_for_signature(self, contract, docuseal_service, manual_price=None, manual_price_description=None):
        """Helper method to send contract for signature."""
        from django.conf import settings
        
        # Get template configuration
        template_config = settings.DOCUSEAL_CONTRACT_SETTINGS['templates'].get(contract.contract_type)
        if not template_config:
            raise ValueError(f"No template configuration found for contract type: {contract.contract_type}")
        
        # Use the pre-configured template ID
        template_id = template_config['template_id']
        requires_jet_icu_signature = template_config.get('requires_jet_icu_signature', False)
        
        # Prepare data for field mapping
        trip_data = {
            'trip_number': contract.trip.trip_number,
            'type': contract.trip.type,
            'estimated_departure_time': str(contract.trip.estimated_departure_time) if contract.trip.estimated_departure_time else '',
            'notes': contract.trip.notes or '',
        }
        
        # Get trip lines data - pass as objects for easier access
        trip_lines_data = list(contract.trip.trip_lines.all().order_by('departure_time_utc'))
        
        # Get quote data if available, otherwise use manual pricing
        quote_data = None
        if contract.trip.quote:
            quote_data = {
                'quoted_amount': str(contract.trip.quote.quoted_amount)
            }
        elif manual_price is not None:
            quote_data = {
                'quoted_amount': str(manual_price)
            }
        
        # Get contact data
        contact_data = None
        if contract.customer_contact:
            contact_data = {
                'first_name': contract.customer_contact.first_name or '',
                'last_name': contract.customer_contact.last_name or '',
                'business_name': contract.customer_contact.business_name or '',
                'email': contract.customer_contact.email or '',
                'phone': contract.customer_contact.phone or '',
                'address_line1': contract.customer_contact.address_line1 or '',
                'address_line2': contract.customer_contact.address_line2 or '',
                'city': contract.customer_contact.city or '',
                'state': contract.customer_contact.state or '',
                'zip': contract.customer_contact.zip or '',
                'country': contract.customer_contact.country or '',
            }
        
        # Get patient data
        patient_data = None
        if contract.patient:
            patient_data = {
                'info': {
                    'first_name': contract.patient.info.first_name or '',
                    'last_name': contract.patient.info.last_name or '',
                    'phone': contract.patient.info.phone or '',
                    'address_line1': contract.patient.info.address_line1 or '',
                    'city': contract.patient.info.city or '',
                    'state': contract.patient.info.state or '',
                    'zip': contract.patient.info.zip or '',
                },
                'date_of_birth': str(contract.patient.date_of_birth) if contract.patient.date_of_birth else '',
                'nationality': contract.patient.nationality or '',
                'passport_number': contract.patient.passport_number or '',
                'special_instructions': contract.patient.special_instructions or '',
            }
        
        # Get passengers data
        passengers = contract.trip.passengers.all()
        passengers_data = []
        for passenger in passengers:
            passengers_data.append({
                'info': {
                    'first_name': passenger.info.first_name or '',
                    'last_name': passenger.info.last_name or '',
                }
            })
        
        # Generate field mappings based on contract type
        fields = docuseal_service.create_contract_fields_mapping(
            contract_type=contract.contract_type,
            trip_data=trip_data,
            trip_lines_data=trip_lines_data,
            contact_data=contact_data,
            patient_data=patient_data,
            passengers_data=passengers_data,
            quote_data=quote_data
        )
        
        # Get roles from template configuration
        customer_role = template_config.get('customer_role', 'patient')
        jet_icu_role = template_config.get('jet_icu_role', 'jet_icu')
        
        # Prepare submitters list - assign fields to JET ICU role as requested
        if requires_jet_icu_signature:
            # For contracts requiring JET ICU signature, customer signs but JET ICU gets the field data
            submitters = [
                {
                    'name': contract.signer_name,
                    'email': contract.signer_email,
                    'role': customer_role,
                    'fields': {}  # Customer doesn't fill fields, just signs
                },
                {
                    'name': 'JET ICU Representative', 
                    'email': settings.DOCUSEAL_JET_ICU_SIGNER_EMAIL,
                    'role': jet_icu_role,
                    'fields': fields  # JET ICU gets all the field data
                }
            ]
        else:
            # For single-signature contracts, assign fields to the JET ICU role (First Party)
            submitters = [
                {
                    'name': contract.signer_name,
                    'email': contract.signer_email, 
                    'role': customer_role,
                    'fields': {}  # Customer signs as Second Party with no fields
                },
                {
                    'name': 'JET ICU Representative',
                    'email': settings.DOCUSEAL_JET_ICU_SIGNER_EMAIL,
                    'role': jet_icu_role,
                    'fields': fields  # JET ICU (First Party) gets all the field data
                }
            ]
        
        # Store template ID in contract
        contract.docuseal_template_id = template_id
        
        # Create submission
        submission_result = docuseal_service.create_submission(
            template_id=template_id,
            submitters=submitters,
            send_email=True
        )
        
        # DocuSeal returns an array of submitters, get the submission_id from the first one
        if isinstance(submission_result, list) and len(submission_result) > 0:
            first_submitter = submission_result[0]
            submission_id = first_submitter.get('submission_id')
            
            # Update contract
            contract.docuseal_submission_id = str(submission_id)
            contract.status = 'pending'
            contract.date_sent = timezone.now()
            contract.docuseal_response_data = {
                'submitters': submission_result,
                'submission_id': submission_id
            }
            contract.save()
            
            logger.info(f"Contract {contract.id} updated with submission_id: {submission_id}")
        else:
            logger.error(f"Unexpected DocuSeal response format: {type(submission_result)}")
            raise ValueError("Unexpected DocuSeal response format")
        
        return submission_result
    
    def _generate_contract_summary(self, contract):
        """Generate a summary of contract details for logging/display."""
        from django.conf import settings
        template_config = settings.DOCUSEAL_CONTRACT_SETTINGS['templates'].get(contract.contract_type, {})
        return {
            'contract_id': str(contract.id),
            'contract_type': contract.contract_type,
            'template_id': template_config.get('template_id'),
            'template_name': template_config.get('name'),
            'trip_number': contract.trip.trip_number,
            'signer_email': contract.signer_email,
            'requires_jet_icu_signature': template_config.get('requires_jet_icu_signature', False)
        }
    
    def _resend_contract(self, contract, docuseal_service):
        """Resend existing contract."""
        # Implementation for resending would go here
        contract.date_sent = timezone.now()
        contract.save()
        return {'status': 'resent'}
    
    def _cancel_contract(self, contract, docuseal_service):
        """Cancel contract."""
        contract.status = 'cancelled'
        contract.save()
        return {'status': 'cancelled'}
    
    def _archive_contract(self, contract, docuseal_service):
        """Archive contract."""
        if contract.docuseal_submission_id:
            result = docuseal_service.archive_submission(contract.docuseal_submission_id)
            contract.status = 'cancelled'
            contract.save()
            return result
        return {'status': 'archived'}


# DocuSeal Webhook Handler
@api_view(['POST'])
@permission_classes([])  # Allow unauthenticated access for webhooks
def docuseal_webhook(request):
    """Handle DocuSeal webhook events."""
    try:
        # Validate webhook (in production, you'd verify the signature)
        webhook_data = request.data
        
        # Process webhook
        docuseal_service = DocuSealService()
        processed_event = docuseal_service.process_webhook_event(webhook_data)
        
        submission_id = processed_event.get('submission_id')
        event_type = processed_event.get('event_type')
        
        if submission_id:
            # Find contract by submission ID
            try:
                contract = Contract.objects.get(docuseal_submission_id=submission_id)
                
                # Update contract based on event type
                if event_type == 'form.completed':
                    contract.status = 'signed'
                    contract.date_signed = timezone.now()
                    
                    # Download signed document
                    try:
                        signed_doc_content = docuseal_service.get_submission_documents(submission_id)
                        
                        # Create Document record for signed document
                        signed_document = Document.objects.create(
                            filename=f"{contract.title}_signed.pdf",
                            content=signed_doc_content,
                            document_type='contract',
                            trip=contract.trip,
                            created_by_id=1  # System user
                        )
                        contract.signed_document = signed_document
                        
                    except Exception as e:
                        logger.error(f"Failed to download signed document: {str(e)}")
                
                elif event_type == 'form.viewed':
                    # Contract was viewed but not necessarily completed
                    pass
                    
                elif event_type == 'form.started':
                    # Signing process started
                    pass
                
                # Update response data
                contract.docuseal_response_data.update({
                    'last_webhook_event': processed_event,
                    'last_webhook_time': timezone.now().isoformat()
                })
                contract.save()
                
                logger.info(f"Updated contract {contract.id} from webhook event {event_type}")
                
            except Contract.DoesNotExist:
                logger.warning(f"No contract found for submission ID: {submission_id}")
        
        return Response({'status': 'processed'}, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"DocuSeal webhook processing failed: {str(e)}")
        return Response({
            'error': 'Webhook processing failed'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# User Activation Token Views
import secrets
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth.models import User
from .models import UserActivationToken
from .serializers import (
    CreateUserWithTokenSerializer, ResendActivationEmailSerializer, VerifyTokenSerializer, VerifyTokenResponseSerializer,
    SetPasswordSerializer, ForgotPasswordSerializer, UserActivationTokenSerializer
)
from utils.smtp.email import send_template, send_user_activation_email, send_password_reset_email


def generate_secure_token():
    """Generate a cryptographically secure random token."""
    return secrets.token_urlsafe(32)


def create_activation_token(user, email, token_type='activation', hours=24):
    """Create an activation or reset token for a user."""
    token = generate_secure_token()
    expires_at = timezone.now() + timedelta(hours=hours)

    return UserActivationToken.objects.create(
        user=user,
        token=token,
        email=email,
        token_type=token_type,
        expires_at=expires_at
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_user_with_token(request):
    """Create a user and send activation email with token."""
    serializer = CreateUserWithTokenSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    data = serializer.validated_data

    try:
        # Check if user with this email already exists
        if User.objects.filter(email=data['email']).exists():
            return Response({
                'error': 'A user with this email already exists.'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Create inactive user (no password initially)
        user = User.objects.create_user(
            username=data['email'],  # Use email as username
            email=data['email'],
            is_active=False  # User must activate via email
        )

        # Create user profile
        from .models import UserProfile, Role
        profile = UserProfile.objects.create(
            user=user,
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            status='pending'
        )

        # Assign roles if provided
        if data.get('role_ids'):
            roles = Role.objects.filter(id__in=data['role_ids'])
            profile.roles.set(roles)

        # If marked as admin, automatically assign Admin role with full permissions
        if data.get('is_admin', False):
            admin_role, created = Role.objects.get_or_create(
                name='Admin',
                defaults={'description': 'Full system administrator with all permissions'}
            )
            profile.roles.add(admin_role)

            # Also mark the Django user as staff for admin interface access
            user.is_staff = True
            user.save()

        # Create activation token
        token_obj = create_activation_token(user, data['email'], 'activation')

        # Send activation email if requested
        if data.get('send_activation_email', True):
            frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:5179')

            try:
                email_sent = send_user_activation_email(
                    email=data['email'],
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    token=token_obj.token,
                    frontend_url=frontend_url
                )
                if not email_sent:
                    logger.error(f"Failed to send activation email to {data['email']}")
            except Exception as e:
                logger.error(f"SMTP error sending activation email to {data['email']}: {str(e)}")
                logger.info(f"Activation token for {data['email']}: {token_obj.token}")
                email_sent = False

        # Prepare success message based on email status
        if data.get('send_activation_email', True):
            if 'email_sent' in locals() and email_sent:
                message = f'User created successfully! Activation email sent to {data["email"]}.'
            else:
                message = f'User created successfully! Note: Activation email could not be sent to {data["email"]}. Please contact IT support.'
        else:
            message = 'User created successfully!'

        # Serialize the created UserProfile to return full data
        from .serializers import UserProfileReadSerializer
        serialized_profile = UserProfileReadSerializer(profile, context={'request': request}).data

        return Response({
            'message': message,
            'user_id': user.id,
            'profile': serialized_profile,
            'token': token_obj.token if not data.get('send_activation_email', True) or not locals().get('email_sent', False) else None
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        # Clean up if user was created but something failed
        if 'user' in locals():
            user.delete()

        return Response({
            'error': f'Failed to create user: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_token(request):
    """Verify an activation or reset token."""
    serializer = VerifyTokenSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    token = serializer.validated_data['token']

    try:
        token_obj = UserActivationToken.objects.get(token=token)

        if not token_obj.is_valid():
            if token_obj.is_used:
                message = 'This token has already been used.'
            else:
                message = 'This token has expired.'

            return Response({
                'valid': False,
                'message': message
            }, status=status.HTTP_400_BAD_REQUEST)

        # Get user info
        user_info = {
            'id': token_obj.user.id,
            'email': token_obj.email,
            'first_name': getattr(token_obj.user.profile, 'first_name', ''),
            'last_name': getattr(token_obj.user.profile, 'last_name', ''),
        }

        response_serializer = VerifyTokenResponseSerializer({
            'valid': True,
            'token_type': token_obj.token_type,
            'email': token_obj.email,
            'user_info': user_info,
            'message': 'Token is valid.'
        })

        return Response(response_serializer.data, status=status.HTTP_200_OK)

    except UserActivationToken.DoesNotExist:
        return Response({
            'valid': False,
            'message': 'Invalid token.'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def resend_activation_email(request):
    """Resend activation email for a user."""
    serializer = ResendActivationEmailSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    data = serializer.validated_data

    try:
        # Get the user profile
        from .models import UserProfile
        profile = UserProfile.objects.get(id=data['user_id'])
        user = profile.user

        # Check if user is already active
        if user.is_active:
            return Response({
                'error': 'User is already active.'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Create new activation token (invalidate old ones)
        UserActivationToken.objects.filter(user=user, token_type='activation').update(is_used=True)
        token_obj = create_activation_token(user, profile.email, 'activation')

        # Send activation email
        frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:5179')

        try:
            email_sent = send_user_activation_email(
                email=profile.email,
                first_name=profile.first_name,
                last_name=profile.last_name,
                token=token_obj.token,
                frontend_url=frontend_url
            )
            if not email_sent:
                logger.error(f"Failed to send activation email to {profile.email}")
        except Exception as e:
            logger.error(f"SMTP error sending activation email to {profile.email}: {str(e)}")
            logger.info(f"Activation token for {profile.email}: {token_obj.token}")
            email_sent = False

        # Prepare success message based on email status
        if 'email_sent' in locals() and email_sent:
            message = f'Activation email sent to {profile.email}.'
        else:
            message = f'Activation token created but email could not be sent to {profile.email}. Please contact IT support.'

        return Response({
            'message': message,
            'token': token_obj.token if not email_sent else None
        }, status=status.HTTP_200_OK)

    except UserProfile.DoesNotExist:
        return Response({
            'error': 'User not found.'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Error resending activation email: {str(e)}")
        return Response({
            'error': f'Failed to resend activation email: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def set_password(request):
    """Set password using activation or reset token."""
    serializer = SetPasswordSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    data = serializer.validated_data

    try:
        token_obj = UserActivationToken.objects.get(token=data['token'])

        if not token_obj.is_valid():
            return Response({
                'error': 'Token is invalid or has expired.'
            }, status=status.HTTP_400_BAD_REQUEST)

        user = token_obj.user

        # Set password
        user.set_password(data['password'])
        user.is_active = True  # Activate user
        user.save()

        # Update profile with phone number if provided
        if data.get('phone'):
            try:
                profile = user.profile
                profile.phone = data['phone']
                profile.status = 'active'
                profile.save()
            except Exception:
                # Create profile if it doesn't exist
                UserProfile.objects.create(
                    user=user,
                    phone=data['phone'],
                    status='active'
                )
        else:
            # Just update status if profile exists
            try:
                profile = user.profile
                profile.status = 'active'
                profile.save()
            except Exception:
                pass

        # Mark token as used
        token_obj.is_used = True
        token_obj.used_at = timezone.now()
        token_obj.save()

        return Response({
            'message': 'Password set successfully. You can now log in.',
            'user_id': user.id
        }, status=status.HTTP_200_OK)

    except UserActivationToken.DoesNotExist:
        return Response({
            'error': 'Invalid token.'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password(request):
    """Send password reset email."""
    serializer = ForgotPasswordSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    email = serializer.validated_data['email']

    try:
        user = User.objects.get(email=email, is_active=True)

        # Create reset token
        token_obj = create_activation_token(user, email, 'password_reset', hours=2)  # 2 hour expiry

        # Send reset email with error handling
        frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:5179')

        try:
            email_sent = send_password_reset_email(
                email=email,
                token=token_obj.token,
                frontend_url=frontend_url
            )

            if not email_sent:
                logger.error(f"Failed to send password reset email to {email}")
        except Exception as e:
            # Log the error but don't fail the request - for security don't reveal SMTP issues
            logger.error(f"SMTP error sending password reset email to {email}: {str(e)}")
            # For debugging purposes when SMTP isn't configured, log the token
            logger.info(f"Password reset token for {email}: {token_obj.token}")

        # Always return success for security - don't reveal whether email actually sent
        return Response({
            'message': 'If an account with this email exists, a password reset email has been sent.'
        }, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        # Don't reveal whether user exists for security
        return Response({
            'message': 'If an account with this email exists, a password reset email has been sent.'
        }, status=status.HTTP_200_OK)


# MFA SMS Verification Endpoints

@api_view(['POST'])
@permission_classes([AllowAny])
def send_sms_code(request):
    """
    Send SMS verification code to phone number
    """
    try:
        from utils.services.twilio_service import twilio_service

        phone_number = request.data.get('phone_number')
        if not phone_number:
            return Response({
                'error': 'Phone number is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Get user if authenticated
        user = request.user if request.user.is_authenticated else None

        result = twilio_service.send_sms_verification_code(phone_number, user)

        if result['success']:
            return Response({
                'message': result['message'],
                'phone_number': result['phone_number'],
                'expires_at': result['expires_at']
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': result['error']
            }, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        logger.error(f"Error in send_sms_code: {str(e)}")
        return Response({
            'error': 'An error occurred while sending SMS'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_sms_code(request):
    """
    Verify SMS code entered by user
    """
    try:
        from utils.services.twilio_service import twilio_service

        phone_number = request.data.get('phone_number')
        code = request.data.get('code')

        if not phone_number or not code:
            return Response({
                'error': 'Phone number and code are required'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Get user if authenticated
        user = request.user if request.user.is_authenticated else None

        result = twilio_service.verify_sms_code(phone_number, code, user)

        if result['success']:
            return Response({
                'message': result['message'],
                'phone_number': result['phone_number']
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': result['error']
            }, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        logger.error(f"Error in verify_sms_code: {str(e)}")
        return Response({
            'error': 'An error occurred while verifying SMS code'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def setup_phone(request):
    """
    Setup and verify phone number for authenticated user
    """
    try:
        from utils.services.twilio_service import twilio_service

        phone_number = request.data.get('phone_number')
        code = request.data.get('code')

        if not phone_number:
            return Response({
                'error': 'Phone number is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        # If code is provided, verify it
        if code:
            result = twilio_service.verify_sms_code(phone_number, code, request.user)

            if result['success']:
                # Update user's phone number and mark as verified
                user_profile = request.user.profile
                user_profile.phone = result['phone_number']
                user_profile.phone_verified = True
                user_profile.save()

                return Response({
                    'message': 'Phone number verified and saved successfully',
                    'phone_number': result['phone_number'],
                    'phone_verified': True
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'error': result['error']
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Send verification code
            result = twilio_service.send_sms_verification_code(phone_number, request.user)

            if result['success']:
                return Response({
                    'message': result['message'],
                    'phone_number': result['phone_number'],
                    'expires_at': result['expires_at']
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'error': result['error']
                }, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        logger.error(f"Error in setup_phone: {str(e)}")
        return Response({
            'error': 'An error occurred while setting up phone'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_with_mfa(request):
    """
    Login with MFA support - handles username/password + SMS verification
    """
    try:
        from utils.services.twilio_service import twilio_service
        from rest_framework_simplejwt.tokens import RefreshToken

        username = request.data.get('username')
        password = request.data.get('password')
        phone_number = request.data.get('phone_number')
        sms_code = request.data.get('sms_code')

        if not username or not password:
            return Response({
                'error': 'Username and password are required'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate user
        user = authenticate(username=username, password=password)
        if not user:
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)

        # Check if user has MFA enabled
        user_profile = getattr(user, 'profile', None)
        if not user_profile:
            return Response({
                'error': 'User profile not found'
            }, status=status.HTTP_400_BAD_REQUEST)

        # If MFA is enabled and user has verified phone
        if user_profile.mfa_enabled and user_profile.phone_verified and user_profile.phone:
            if not sms_code:
                # Send SMS code and return intermediate response
                result = twilio_service.send_sms_verification_code(user_profile.phone, user)

                if result['success']:
                    return Response({
                        'mfa_required': True,
                        'phone_number': result['phone_number'],
                        'message': 'SMS verification code sent'
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        'error': result['error']
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                # Verify SMS code
                result = twilio_service.verify_sms_code(user_profile.phone, sms_code, user)

                if not result['success']:
                    return Response({
                        'error': result['error']
                    }, status=status.HTTP_400_BAD_REQUEST)

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        return Response({
            'access': str(access_token),
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user_profile.first_name if user_profile else '',
                'last_name': user_profile.last_name if user_profile else '',
                'mfa_enabled': user_profile.mfa_enabled if user_profile else False,
                'phone_verified': user_profile.phone_verified if user_profile else False
            }
        }, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Error in login_with_mfa: {str(e)}")
        return Response({
            'error': 'An error occurred during login'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
