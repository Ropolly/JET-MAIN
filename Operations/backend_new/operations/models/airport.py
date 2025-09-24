from core.models import BaseModel
from django.db import models

class AirportType(models.TextChoices):
    LARGE = 'large_airport', 'Large airport'
    MEDIUM = 'medium_airport', 'Medium airport'
    SMALL = 'small_airport', 'Small airport'

class Airport(BaseModel):
    ident = models.CharField(max_length=10, unique=True, db_index=True)
    name = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    elevation = models.IntegerField(blank=True, null=True)
    iso_country = models.CharField(max_length=100)
    iso_region = models.CharField(max_length=100, blank=True, null=True)
    municipality = models.CharField(max_length=100, blank=True, null=True)
    icao_code = models.CharField(max_length=4, unique=True, db_index=True, blank=True, null=True)
    iata_code = models.CharField(max_length=3, db_index=True, blank=True, null=True)
    local_code = models.CharField(max_length=10, blank=True, null=True)
    gps_code = models.CharField(max_length=20, blank=True, null=True)
    airport_type = models.CharField(
        max_length=20,
        choices=AirportType.choices,
        default=AirportType.SMALL,
        db_index=True,
    )
    fbos = models.ManyToManyField(FBO, related_name="airports", blank=True)
    grounds = models.ManyToManyField(Ground, related_name="airports", blank=True)

    timezone = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} ({self.icao_code}/{self.iata_code})"