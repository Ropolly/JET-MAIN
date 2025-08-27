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
    Patient, Quote, Passenger, CrewLine, Trip, TripLine, Staff, StaffRole, StaffRoleMembership, TripEvent
)
from .contact_service import ContactCreationService, ContactCreationSerializer
from .serializers import (
    ModificationSerializer, PermissionSerializer, RoleSerializer, DepartmentSerializer,
    ContactSerializer, FBOSerializer, GroundSerializer, AirportSerializer, AircraftSerializer,
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
        serializer.save(created_by=self.request.user)

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
    
    def get_serializer_class(self):
        if self.action in ('list', 'retrieve', 'trip_lines'):
            return TripReadSerializer
        return TripWriteSerializer
    
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
