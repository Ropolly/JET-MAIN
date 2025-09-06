"""
Admin configuration for aircraft app.
"""
from django.contrib import admin
from .models import Aircraft, MaintenanceLog


@admin.register(Aircraft)
class AircraftAdmin(admin.ModelAdmin):
    """Admin configuration for Aircraft model."""
    list_display = ('tail_number', 'aircraft_type', 'manufacturer', 'model', 'year_manufactured', 'is_active')
    list_filter = ('manufacturer', 'is_active', 'year_manufactured', 'created_at')
    search_fields = ('tail_number', 'aircraft_type', 'manufacturer', 'model', 'serial_number')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('tail_number', 'aircraft_type', 'manufacturer', 'model', 'serial_number', 'year_manufactured')
        }),
        ('Specifications', {
            'fields': ('max_passengers', 'max_range_nm', 'cruise_speed_kts', 'fuel_capacity_gallons')
        }),
        ('Weight & Balance', {
            'fields': ('empty_weight_lbs', 'max_takeoff_weight_lbs', 'max_landing_weight_lbs')
        }),
        ('Operational Details', {
            'fields': ('home_base', 'insurance_policy', 'registration_expiry', 'annual_inspection_due')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(MaintenanceLog)
class MaintenanceLogAdmin(admin.ModelAdmin):
    """Admin configuration for MaintenanceLog model."""
    list_display = ('aircraft', 'maintenance_type', 'date_performed', 'performed_by', 'cost', 'is_completed')
    list_filter = ('maintenance_type', 'is_completed', 'date_performed', 'created_at')
    search_fields = ('aircraft__tail_number', 'description', 'performed_by', 'part_numbers')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'date_performed'
    
    fieldsets = (
        ('Maintenance Information', {
            'fields': ('aircraft', 'maintenance_type', 'date_performed', 'performed_by')
        }),
        ('Details', {
            'fields': ('description', 'part_numbers', 'hours_at_maintenance', 'next_due_hours')
        }),
        ('Cost & Completion', {
            'fields': ('cost', 'is_completed', 'completion_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
