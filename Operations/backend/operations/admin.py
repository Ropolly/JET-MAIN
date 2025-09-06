from django.contrib import admin
from .models import Quote, Patient, Passenger, CrewLine, Trip, TripLine, TripEvent


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'quoted_amount', 'contact', 'pickup_airport', 
        'dropoff_airport', 'status', 'payment_status', 'inquiry_date'
    ]
    list_filter = ['status', 'payment_status', 'aircraft_type', 'medical_team']
    search_fields = ['contact__business_name', 'contact__first_name', 'contact__last_name']
    readonly_fields = ['id', 'created_on', 'modified_on']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('contact', 'quoted_amount', 'status', 'payment_status')
        }),
        ('Flight Details', {
            'fields': (
                'pickup_airport', 'dropoff_airport', 'aircraft_type',
                'estimated_flight_time', 'medical_team', 'includes_grounds',
                'number_of_stops'
            )
        }),
        ('Cruise Information', {
            'fields': (
                'cruise_doctor_first_name', 'cruise_doctor_last_name',
                'cruise_line', 'cruise_ship'
            ),
            'classes': ('collapse',)
        }),
        ('Documents & Agreements', {
            'fields': (
                'quote_pdf', 'quote_pdf_status', 'quote_pdf_email',
                'payment_agreement', 'consent_for_transport',
                'patient_service_agreement'
            ),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('id', 'created_on', 'modified_on'),
            'classes': ('collapse',)
        })
    )


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'info', 'date_of_birth', 'nationality', 
        'passport_number', 'status'
    ]
    list_filter = ['status', 'nationality', 'bed_at_origin', 'bed_at_destination']
    search_fields = ['info__first_name', 'info__last_name', 'passport_number']
    readonly_fields = ['id', 'created_on', 'modified_on']
    
    fieldsets = (
        ('Patient Information', {
            'fields': ('info', 'date_of_birth', 'nationality', 'status')
        }),
        ('Medical Requirements', {
            'fields': ('bed_at_origin', 'bed_at_destination', 'special_instructions')
        }),
        ('Travel Documents', {
            'fields': (
                'passport_number', 'passport_expiration_date',
                'passport_document', 'letter_of_medical_necessity'
            )
        }),
        ('Metadata', {
            'fields': ('id', 'created_on', 'modified_on'),
            'classes': ('collapse',)
        })
    )


@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    list_display = ['id', 'info', 'date_of_birth', 'nationality', 'contact_number']
    search_fields = ['info__first_name', 'info__last_name', 'passport_number']
    readonly_fields = ['id', 'created_on', 'modified_on']


@admin.register(CrewLine)
class CrewLineAdmin(admin.ModelAdmin):
    list_display = ['id', 'primary_in_command', 'secondary_in_command']
    search_fields = [
        'primary_in_command__first_name', 'primary_in_command__last_name',
        'secondary_in_command__first_name', 'secondary_in_command__last_name'
    ]
    readonly_fields = ['id', 'created_on', 'modified_on']
    
    fieldsets = (
        ('Crew Assignment', {
            'fields': ('primary_in_command', 'secondary_in_command', 'medic_ids')
        }),
        ('Metadata', {
            'fields': ('id', 'created_on', 'modified_on'),
            'classes': ('collapse',)
        })
    )


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = [
        'trip_number', 'type', 'status', 'aircraft', 
        'estimated_departure_time', 'created_on'
    ]
    list_filter = ['type', 'status']
    search_fields = ['trip_number', 'notes']
    readonly_fields = ['id', 'created_on', 'modified_on']
    
    fieldsets = (
        ('Trip Information', {
            'fields': ('trip_number', 'type', 'status', 'notes')
        }),
        ('Related Entities', {
            'fields': ('quote', 'patient', 'aircraft', 'passengers')
        }),
        ('Timing', {
            'fields': (
                'estimated_departure_time', 'pre_flight_duty_time',
                'post_flight_duty_time'
            )
        }),
        ('Documents', {
            'fields': ('internal_itinerary', 'customer_itinerary'),
            'classes': ('collapse',)
        }),
        ('Communication', {
            'fields': ('email_chain',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('id', 'created_on', 'modified_on'),
            'classes': ('collapse',)
        })
    )


@admin.register(TripLine)
class TripLineAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'trip', 'origin_airport', 'destination_airport',
        'departure_time_local', 'arrival_time_local', 'passenger_leg'
    ]
    list_filter = ['passenger_leg', 'origin_airport', 'destination_airport']
    search_fields = ['trip__trip_number']
    readonly_fields = ['id', 'created_on', 'modified_on']
    
    fieldsets = (
        ('Flight Information', {
            'fields': (
                'trip', 'origin_airport', 'destination_airport',
                'departure_fbo', 'arrival_fbo', 'crew_line'
            )
        }),
        ('Timing', {
            'fields': (
                'departure_time_local', 'departure_time_utc',
                'arrival_time_local', 'arrival_time_utc'
            )
        }),
        ('Flight Details', {
            'fields': ('distance', 'flight_time', 'ground_time', 'passenger_leg')
        }),
        ('Metadata', {
            'fields': ('id', 'created_on', 'modified_on'),
            'classes': ('collapse',)
        })
    )


@admin.register(TripEvent)
class TripEventAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'trip', 'event_type', 'airport',
        'start_time_local', 'end_time_local'
    ]
    list_filter = ['event_type', 'airport']
    search_fields = ['trip__trip_number', 'notes']
    readonly_fields = ['id', 'created_on', 'modified_on']
    
    fieldsets = (
        ('Event Information', {
            'fields': ('trip', 'event_type', 'airport', 'crew_line')
        }),
        ('Timing', {
            'fields': (
                'start_time_local', 'start_time_utc',
                'end_time_local', 'end_time_utc'
            )
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Metadata', {
            'fields': ('id', 'created_on', 'modified_on'),
            'classes': ('collapse',)
        })
    )
