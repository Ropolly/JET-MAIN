from django.db import models
from common.models import BaseModel
import math


class AirportType(models.TextChoices):
    """Airport type choices."""
    LARGE = 'large_airport', 'Large airport'
    MEDIUM = 'medium_airport', 'Medium airport'
    SMALL = 'small_airport', 'Small airport'


class Airport(BaseModel):
    """Airport model with location and operational data."""
    ident = models.CharField(max_length=10, unique=True, db_index=True)
    name = models.CharField(max_length=255)
    
    # Geographic coordinates
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    elevation = models.IntegerField(blank=True, null=True)
    
    # Location information
    iso_country = models.CharField(max_length=100)
    iso_region = models.CharField(max_length=100, blank=True, null=True)
    municipality = models.CharField(max_length=100, blank=True, null=True)
    
    # Airport codes
    icao_code = models.CharField(max_length=4, unique=True, db_index=True, blank=True, null=True)
    iata_code = models.CharField(max_length=3, db_index=True, blank=True, null=True)
    local_code = models.CharField(max_length=10, blank=True, null=True)
    gps_code = models.CharField(max_length=20, blank=True, null=True)
    
    # Airport classification
    airport_type = models.CharField(
        max_length=20,
        choices=AirportType.choices,
        default=AirportType.SMALL,
        db_index=True,
    )
    
    # Timezone for proper time calculations
    timezone = models.CharField(max_length=50)
    
    # Related services
    fbos = models.ManyToManyField('contacts.FBO', related_name="airports", blank=True)
    grounds = models.ManyToManyField('contacts.Ground', related_name="airports", blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['ident']),
            models.Index(fields=['icao_code']),
            models.Index(fields=['iata_code']),
            models.Index(fields=['airport_type']),
            models.Index(fields=['iso_country']),
        ]

    def __str__(self):
        codes = []
        if self.icao_code:
            codes.append(self.icao_code)
        if self.iata_code:
            codes.append(self.iata_code)
        code_str = "/".join(codes) if codes else self.ident
        return f"{self.name} ({code_str})"
    
    @property
    def primary_code(self):
        """Return the primary airport code (ICAO preferred, then IATA, then ident)."""
        return self.icao_code or self.iata_code or self.ident
    
    def calculate_distance_to(self, other_airport):
        """
        Calculate great circle distance to another airport in nautical miles.
        
        Args:
            other_airport: Another Airport instance
            
        Returns:
            Distance in nautical miles
        """
        if not isinstance(other_airport, Airport):
            raise ValueError("other_airport must be an Airport instance")
        
        # Convert to radians
        lat1 = math.radians(float(self.latitude))
        lon1 = math.radians(float(self.longitude))
        lat2 = math.radians(float(other_airport.latitude))
        lon2 = math.radians(float(other_airport.longitude))
        
        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        # Earth's radius in nautical miles
        earth_radius_nm = 3440.065
        
        return c * earth_radius_nm
    
    def get_nearby_airports(self, radius_nm=50):
        """
        Get airports within a specified radius.
        
        Args:
            radius_nm: Radius in nautical miles
            
        Returns:
            QuerySet of nearby airports
        """
        # This is a simplified implementation
        # In production, you'd use PostGIS or similar for efficient spatial queries
        nearby_airports = []
        
        for airport in Airport.objects.exclude(id=self.id):
            distance = self.calculate_distance_to(airport)
            if distance <= radius_nm:
                nearby_airports.append(airport.id)
        
        return Airport.objects.filter(id__in=nearby_airports)


class WeatherData(BaseModel):
    """Weather data for airports (from scraping services)."""
    airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="weather_data")
    
    # Weather conditions
    temperature_celsius = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    wind_speed_knots = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    wind_direction_degrees = models.IntegerField(null=True, blank=True)
    visibility_miles = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Pressure and humidity
    barometric_pressure_inhg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    humidity_percent = models.IntegerField(null=True, blank=True)
    
    # Conditions
    conditions = models.CharField(max_length=100, blank=True, null=True)  # Clear, Cloudy, Rain, etc.
    ceiling_feet = models.IntegerField(null=True, blank=True)
    
    # Metadata
    observation_time = models.DateTimeField()
    source = models.CharField(max_length=50, default='METAR')  # METAR, TAF, etc.
    raw_data = models.TextField(blank=True, null=True)  # Original weather report
    
    class Meta:
        indexes = [
            models.Index(fields=['airport', 'observation_time']),
            models.Index(fields=['source']),
        ]
        ordering = ['-observation_time']
    
    def __str__(self):
        return f"Weather for {self.airport.primary_code} at {self.observation_time}"
