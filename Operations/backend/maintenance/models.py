from django.db import models


class Aircraft(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('maintenance', 'In Maintenance'),
        ('grounded', 'Grounded'),
    ]
    
    registration = models.CharField(max_length=20, unique=True)
    aircraft_type = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    last_maintenance_date = models.DateField(null=True, blank=True)
    next_maintenance_date = models.DateField(null=True, blank=True)
    total_flight_hours = models.FloatField(default=0)
    manufacturing_date = models.DateField(null=True, blank=True)
    capacity = models.IntegerField(default=0)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.registration} - {self.aircraft_type}"


class MaintenanceLog(models.Model):
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE, related_name='maintenance_logs')
    maintenance_date = models.DateField()
    description = models.TextField()
    performed_by = models.CharField(max_length=100)
    hours_spent = models.FloatField(default=0)
    parts_replaced = models.TextField(blank=True)
    is_scheduled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.aircraft.registration} - {self.maintenance_date}"
