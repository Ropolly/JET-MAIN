"""
Admin configuration for airports app.
"""
from django.contrib import admin
from .models import Airport, WeatherData


@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    """Admin configuration for Airport model."""
    list_display = ('icao_code', 'iata_code', 'name', 'city', 'state', 'country', 'is_active')
    list_filter = ('country', 'state', 'is_active', 'created_at')
    search_fields = ('icao_code', 'iata_code', 'name', 'city', 'state', 'country')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Identification', {
            'fields': ('icao_code', 'iata_code', 'ident', 'name')
        }),
        ('Location', {
            'fields': ('city', 'state', 'country', 'latitude', 'longitude', 'elevation')
        }),
        ('Operational Details', {
            'fields': ('timezone', 'type', 'municipality', 'scheduled_service')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    """Admin configuration for WeatherData model."""
    list_display = ('airport', 'observation_time', 'temperature_c', 'wind_speed_kts', 'visibility_sm')
    list_filter = ('observation_time', 'created_at')
    search_fields = ('airport__icao_code', 'airport__name', 'metar_raw', 'taf_raw')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'observation_time'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('airport', 'observation_time', 'data_source')
        }),
        ('Weather Conditions', {
            'fields': ('temperature_c', 'dewpoint_c', 'wind_direction_deg', 'wind_speed_kts', 'wind_gust_kts')
        }),
        ('Visibility & Pressure', {
            'fields': ('visibility_sm', 'altimeter_in_hg', 'conditions')
        }),
        ('Raw Data', {
            'fields': ('metar_raw', 'taf_raw'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
