from django.shortcuts import render
from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
import json
from itertools import chain
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from io import BytesIO
import logging
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
    Patient, Quote, Passenger, CrewLine, Trip, TripLine, Staff, StaffRole, StaffRoleMembership, TripEvent, Comment, Contract
)
from .utils import track_creation, track_deletion
from .contact_service import ContactCreationService, ContactCreationSerializer
from utils.services.docuseal_service import DocuSealService

logger = logging.getLogger(__name__)
from .serializers import (
    ModificationSerializer, PermissionSerializer, RoleSerializer, DepartmentSerializer,
    ContactSerializer, CommentSerializer, FBOSerializer, GroundSerializer, AirportSerializer, AircraftSerializer,
    AgreementSerializer, DocumentSerializer,
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
    PatientReadSerializer, PatientWriteSerializer, StaffReadSerializer, StaffWriteSerializer,
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
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
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
            # Exclude system fields that shouldn't be tracked
            excluded_fields = {'id', 'created_on', 'modified_on', 'created_by', 'modified_by'}
            old_fields = {field.name: getattr(old_instance, field.name) 
                         for field in old_instance._meta.fields 
                         if not field.is_relation and field.name not in excluded_fields}
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
            # Use same excluded fields for new values
            excluded_fields = {'id', 'created_on', 'modified_on', 'created_by', 'modified_by'}
            new_fields = {field.name: getattr(instance, field.name) 
                         for field in instance._meta.fields 
                         if not field.is_relation and field.name not in excluded_fields}
            
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
    serializer_class = ContactSerializer
    search_fields = ['first_name', 'last_name', 'business_name', 'email']
    ordering_fields = ['first_name', 'last_name', 'business_name', 'created_on']

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
class PatientViewSet(BaseViewSet):
    queryset = Patient.objects.select_related('info')
    search_fields = ['info__first_name', 'info__last_name', 'nationality']
    ordering_fields = ['created_on']
    permission_classes = [
        permissions.IsAuthenticated,
        CanReadPatient | CanWritePatient | CanModifyPatient | CanDeletePatient
    ]
    
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
        elif self.action in ['update', 'partial_update', 'generate_itineraries']:
            permission_classes = [permissions.IsAuthenticated, CanModifyTrip]
        elif self.action == 'destroy':
            permission_classes = [permissions.IsAuthenticated, CanDeleteTrip]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    @action(detail=True, methods=['post'])
    def generate_itineraries(self, request, pk=None):
        trip = self.get_object()
        # Here you would generate the itineraries
        # This is a placeholder for the actual itinerary generation logic
        serializer = self.get_serializer(trip)
        return Response(serializer.data)
    
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
    
    @action(detail=True, methods=['post'])
    def generate_documents(self, request, pk=None):
        """
        Generate documents for a trip.
        Accepts optional 'document_type' in request body to generate specific document.
        If no document_type provided, generates all applicable documents.
        """
        from utils.docgen.trip_document_generator import TripDocumentGenerator
        from .serializers import DocumentSerializer, DocumentCreateSerializer
        
        trip = self.get_object()
        
        # Validate request data
        serializer = DocumentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        document_type = serializer.validated_data.get('document_type')
        
        try:
            generator = TripDocumentGenerator(str(trip.id), user=request.user)
            
            if document_type:
                # Generate specific document type
                doc = generator.generate_document(document_type)
                if doc:
                    return Response({
                        'message': f'Document {document_type} generated successfully',
                        'documents': DocumentSerializer([doc], many=True).data
                    }, status=status.HTTP_201_CREATED)
                else:
                    return Response({
                        'error': f'Document type {document_type} not applicable for this trip'
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                # Generate all applicable documents
                docs = generator.generate_all_documents()
                return Response({
                    'message': f'{len(docs)} documents generated successfully',
                    'documents': DocumentSerializer(docs, many=True).data
                }, status=status.HTTP_201_CREATED)
                
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
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
                'contact': ContactSerializer(contact).data,
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
                response_data['customer'] = ContactSerializer(related_instance).data
            
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
