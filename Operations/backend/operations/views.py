from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.utils import timezone

from .models import Quote, Patient, Passenger, CrewLine, Trip, TripLine, TripEvent
from .serializers import (
    QuoteSerializer, PatientSerializer, PassengerSerializer,
    CrewLineSerializer, TripSerializer, TripLineSerializer,
    TripEventSerializer, TripTimelineSerializer
)
from .services.trip_service import TripService, CrewService
from .services.quote_service import QuoteService, PatientService


class QuoteViewSet(viewsets.ModelViewSet):
    """ViewSet for Quote operations."""
    
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter quotes based on user permissions and query parameters."""
        queryset = super().get_queryset()
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by payment status
        payment_status = self.request.query_params.get('payment_status')
        if payment_status:
            queryset = queryset.filter(payment_status=payment_status)
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date:
            queryset = queryset.filter(inquiry_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(inquiry_date__lte=end_date)
        
        return queryset.select_related('contact', 'pickup_airport', 'dropoff_airport', 'patient')
    
    def perform_create(self, serializer):
        """Create quote using service layer."""
        quote_data = serializer.validated_data
        
        # Use service to create quote with business logic
        quote = QuoteService.create_quote(
            contact_id=quote_data['contact'].id,
            pickup_airport_id=quote_data['pickup_airport'].id,
            dropoff_airport_id=quote_data['dropoff_airport'].id,
            aircraft_type=quote_data['aircraft_type'],
            medical_team=quote_data['medical_team'],
            estimated_flight_time=quote_data['estimated_flight_time'],
            **{k: v for k, v in quote_data.items() if k not in [
                'contact', 'pickup_airport', 'dropoff_airport'
            ]}
        )
        
        serializer.instance = quote
    
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """Update quote status with validation."""
        quote = self.get_object()
        new_status = request.data.get('status')
        
        if not new_status:
            return Response(
                {'error': 'Status is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            updated_quote = QuoteService.update_quote_status(
                quote, new_status, request.user
            )
            serializer = self.get_serializer(updated_quote)
            return Response(serializer.data)
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def generate_pdf(self, request, pk=None):
        """Generate PDF document for quote."""
        quote = self.get_object()
        
        try:
            document_id = QuoteService.generate_quote_pdf(quote)
            return Response({
                'document_id': document_id,
                'message': 'PDF generated successfully'
            })
        except Exception as e:
            return Response(
                {'error': f'Failed to generate PDF: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['get'])
    def payment_schedule(self, request, pk=None):
        """Get payment schedule for quote."""
        quote = self.get_object()
        schedule = QuoteService.calculate_payment_schedule(quote)
        return Response(schedule)


class PatientViewSet(viewsets.ModelViewSet):
    """ViewSet for Patient operations."""
    
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter patients based on query parameters."""
        queryset = super().get_queryset()
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset.select_related('info')
    
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """Update patient status with validation."""
        patient = self.get_object()
        new_status = request.data.get('status')
        
        if not new_status:
            return Response(
                {'error': 'Status is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            updated_patient = PatientService.update_patient_status(
                patient, new_status, request.user
            )
            serializer = self.get_serializer(updated_patient)
            return Response(serializer.data)
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['get'])
    def validate_documents(self, request, pk=None):
        """Validate patient medical documents."""
        patient = self.get_object()
        validation_results = PatientService.validate_medical_documents(patient)
        return Response(validation_results)


class PassengerViewSet(viewsets.ModelViewSet):
    """ViewSet for Passenger operations."""
    
    queryset = Passenger.objects.all()
    serializer_class = PassengerSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Get passengers with related contact information."""
        return super().get_queryset().select_related('info')


class CrewLineViewSet(viewsets.ModelViewSet):
    """ViewSet for CrewLine operations."""
    
    queryset = CrewLine.objects.all()
    serializer_class = CrewLineSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Get crew lines with related contact information."""
        return super().get_queryset().select_related(
            'primary_in_command', 'secondary_in_command'
        ).prefetch_related('medic_ids')
    
    def perform_create(self, serializer):
        """Create crew line using service layer."""
        crew_data = serializer.validated_data
        
        try:
            crew_line = CrewService.create_crew_line(
                primary_pic_id=crew_data['primary_in_command'].id,
                secondary_sic_id=crew_data['secondary_in_command'].id,
                medic_ids=[medic.id for medic in crew_data.get('medic_ids', [])]
            )
            serializer.instance = crew_line
        except ValueError as e:
            raise serializers.ValidationError(str(e))
    
    @action(detail=True, methods=['post'])
    def check_availability(self, request, pk=None):
        """Check crew availability for given time period."""
        crew_line = self.get_object()
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')
        
        if not start_time or not end_time:
            return Response(
                {'error': 'start_time and end_time are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            start_datetime = timezone.datetime.fromisoformat(start_time.replace('Z', '+00:00'))
            end_datetime = timezone.datetime.fromisoformat(end_time.replace('Z', '+00:00'))
            
            availability = CrewService.validate_crew_availability(
                crew_line, start_datetime, end_datetime
            )
            return Response(availability)
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class TripViewSet(viewsets.ModelViewSet):
    """ViewSet for Trip operations."""
    
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Get trips with related information."""
        queryset = super().get_queryset()
        
        # Filter by type
        trip_type = self.request.query_params.get('type')
        if trip_type:
            queryset = queryset.filter(type=trip_type)
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date:
            queryset = queryset.filter(estimated_departure_time__gte=start_date)
        if end_date:
            queryset = queryset.filter(estimated_departure_time__lte=end_date)
        
        return queryset.select_related(
            'quote', 'patient', 'aircraft'
        ).prefetch_related('trip_lines', 'events', 'passengers')
    
    def perform_create(self, serializer):
        """Create trip using service layer."""
        trip_data = serializer.validated_data
        
        try:
            trip = TripService.create_trip(
                trip_number=trip_data.get('trip_number', ''),
                trip_type=trip_data['type'],
                aircraft_id=trip_data.get('aircraft').id if trip_data.get('aircraft') else None,
                quote_id=trip_data.get('quote').id if trip_data.get('quote') else None,
                patient_id=trip_data.get('patient').id if trip_data.get('patient') else None,
                **{k: v for k, v in trip_data.items() if k not in [
                    'type', 'aircraft', 'quote', 'patient'
                ]}
            )
            serializer.instance = trip
        except ValueError as e:
            raise serializers.ValidationError(str(e))
    
    @action(detail=True, methods=['post'])
    def add_trip_line(self, request, pk=None):
        """Add a flight leg to the trip."""
        trip = self.get_object()
        
        required_fields = [
            'origin_airport_id', 'destination_airport_id',
            'departure_time_local', 'arrival_time_local'
        ]
        
        for field in required_fields:
            if field not in request.data:
                return Response(
                    {'error': f'{field} is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        try:
            trip_line = TripService.add_trip_line(
                trip=trip,
                origin_airport_id=request.data['origin_airport_id'],
                destination_airport_id=request.data['destination_airport_id'],
                departure_time_local=timezone.datetime.fromisoformat(
                    request.data['departure_time_local'].replace('Z', '+00:00')
                ),
                arrival_time_local=timezone.datetime.fromisoformat(
                    request.data['arrival_time_local'].replace('Z', '+00:00')
                ),
                crew_line_id=request.data.get('crew_line_id'),
                **{k: v for k, v in request.data.items() if k not in required_fields + ['crew_line_id']}
            )
            
            serializer = TripLineSerializer(trip_line)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'])
    def add_crew_change(self, request, pk=None):
        """Add a crew change event to the trip."""
        trip = self.get_object()
        
        required_fields = ['airport_id', 'new_crew_line_id', 'event_time_local']
        
        for field in required_fields:
            if field not in request.data:
                return Response(
                    {'error': f'{field} is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        try:
            event = TripService.add_crew_change_event(
                trip=trip,
                airport_id=request.data['airport_id'],
                new_crew_line_id=request.data['new_crew_line_id'],
                event_time_local=timezone.datetime.fromisoformat(
                    request.data['event_time_local'].replace('Z', '+00:00')
                ),
                notes=request.data.get('notes')
            )
            
            serializer = TripEventSerializer(event)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['get'])
    def timeline(self, request, pk=None):
        """Get chronological timeline of trip events."""
        trip = self.get_object()
        timeline = TripService.get_trip_timeline(trip)
        serializer = TripTimelineSerializer(timeline, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def duration(self, request, pk=None):
        """Get total trip duration."""
        trip = self.get_object()
        duration = TripService.calculate_trip_duration(trip)
        
        if duration:
            return Response({
                'total_duration_seconds': duration.total_seconds(),
                'total_duration_hours': duration.total_seconds() / 3600
            })
        else:
            return Response({
                'total_duration_seconds': None,
                'total_duration_hours': None,
                'message': 'No trip lines found'
            })


class TripLineViewSet(viewsets.ModelViewSet):
    """ViewSet for TripLine operations."""
    
    queryset = TripLine.objects.all()
    serializer_class = TripLineSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Get trip lines with related information."""
        queryset = super().get_queryset()
        
        # Filter by trip
        trip_id = self.request.query_params.get('trip_id')
        if trip_id:
            queryset = queryset.filter(trip_id=trip_id)
        
        return queryset.select_related(
            'trip', 'origin_airport', 'destination_airport',
            'departure_fbo', 'arrival_fbo', 'crew_line'
        )


class TripEventViewSet(viewsets.ModelViewSet):
    """ViewSet for TripEvent operations."""
    
    queryset = TripEvent.objects.all()
    serializer_class = TripEventSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Get trip events with related information."""
        queryset = super().get_queryset()
        
        # Filter by trip
        trip_id = self.request.query_params.get('trip_id')
        if trip_id:
            queryset = queryset.filter(trip_id=trip_id)
        
        # Filter by event type
        event_type = self.request.query_params.get('event_type')
        if event_type:
            queryset = queryset.filter(event_type=event_type)
        
        return queryset.select_related('trip', 'airport', 'crew_line')
