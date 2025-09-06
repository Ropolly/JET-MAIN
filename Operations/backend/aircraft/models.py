from django.db import models
from common.models import BaseModel
from decimal import Decimal


class Aircraft(BaseModel):
    """Aircraft model for fleet management."""
    tail_number = models.CharField(max_length=20, unique=True, db_index=True)
    company = models.CharField(max_length=255)
    
    # Aircraft specifications
    mgtow = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Maximum Gross Takeoff Weight"
    )
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100)
    
    # Registration and certification
    registration_country = models.CharField(max_length=3, default='US')
    year_manufactured = models.IntegerField(null=True, blank=True)
    
    # Operational specifications
    max_passengers = models.IntegerField(null=True, blank=True)
    max_range_nm = models.IntegerField(null=True, blank=True, verbose_name="Maximum Range (NM)")
    cruise_speed_knots = models.IntegerField(null=True, blank=True)
    service_ceiling_feet = models.IntegerField(null=True, blank=True)
    
    # Status and availability
    operational_status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('maintenance', 'In Maintenance'),
        ('inactive', 'Inactive'),
        ('retired', 'Retired')
    ], default='active')
    
    # Medical equipment configuration
    medical_equipped = models.BooleanField(default=False)
    stretcher_capacity = models.IntegerField(default=0)
    
    # Notes and additional information
    notes = models.TextField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['tail_number']),
            models.Index(fields=['make', 'model']),
            models.Index(fields=['operational_status']),
        ]

    def __str__(self):
        return f"{self.tail_number} - {self.make} {self.model}"
    
    @property
    def is_available(self):
        """Check if aircraft is available for operations."""
        return self.operational_status == 'active'
    
    @property
    def full_designation(self):
        """Return full aircraft designation."""
        return f"{self.make} {self.model} ({self.tail_number})"


class MaintenanceLog(BaseModel):
    """Maintenance log entries for aircraft."""
    
    MAINTENANCE_TYPES = [
        ('inspection', 'Inspection'),
        ('repair', 'Repair'),
        ('modification', 'Modification'),
        ('overhaul', 'Overhaul'),
        ('ad_compliance', 'AD Compliance'),
        ('sb_compliance', 'SB Compliance'),
    ]
    
    MAINTENANCE_STATUS = [
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('deferred', 'Deferred'),
        ('cancelled', 'Cancelled'),
    ]
    
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE, related_name="maintenance_logs")
    
    # Maintenance details
    maintenance_type = models.CharField(max_length=20, choices=MAINTENANCE_TYPES)
    description = models.TextField()
    work_order_number = models.CharField(max_length=50, blank=True, null=True)
    
    # Scheduling
    scheduled_date = models.DateTimeField()
    started_date = models.DateTimeField(null=True, blank=True)
    completed_date = models.DateTimeField(null=True, blank=True)
    
    # Status and tracking
    status = models.CharField(max_length=20, choices=MAINTENANCE_STATUS, default='scheduled')
    priority = models.CharField(max_length=10, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical')
    ], default='medium')
    
    # Personnel and costs
    technician = models.ForeignKey(
        'contacts.Contact', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name="maintenance_work"
    )
    estimated_hours = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    actual_hours = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    actual_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Compliance and documentation
    regulatory_reference = models.CharField(max_length=100, blank=True, null=True)
    compliance_due_date = models.DateField(null=True, blank=True)
    next_due_date = models.DateField(null=True, blank=True)
    
    # Parts and materials
    parts_used = models.JSONField(default=list, blank=True)
    
    # Documentation
    work_performed = models.TextField(blank=True, null=True)
    discrepancies_found = models.TextField(blank=True, null=True)
    corrective_action = models.TextField(blank=True, null=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['aircraft', 'scheduled_date']),
            models.Index(fields=['status', 'priority']),
            models.Index(fields=['maintenance_type']),
            models.Index(fields=['compliance_due_date']),
        ]
        ordering = ['-scheduled_date']
    
    def __str__(self):
        return f"{self.aircraft.tail_number} - {self.get_maintenance_type_display()} - {self.scheduled_date.date()}"
    
    @property
    def is_overdue(self):
        """Check if maintenance is overdue."""
        if self.status in ['completed', 'cancelled']:
            return False
        
        from django.utils import timezone
        return self.scheduled_date < timezone.now()
    
    @property
    def duration_hours(self):
        """Calculate actual duration of maintenance work."""
        if self.started_date and self.completed_date:
            duration = self.completed_date - self.started_date
            return duration.total_seconds() / 3600
        return None


class AircraftDocument(BaseModel):
    """Documents associated with aircraft (certificates, manuals, etc.)."""
    
    DOCUMENT_TYPES = [
        ('certificate', 'Certificate'),
        ('manual', 'Manual'),
        ('logbook', 'Logbook'),
        ('inspection', 'Inspection Report'),
        ('insurance', 'Insurance'),
        ('registration', 'Registration'),
        ('other', 'Other'),
    ]
    
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE, related_name="documents")
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    
    # Document file reference
    document_file = models.ForeignKey(
        'documents.Document', 
        on_delete=models.CASCADE, 
        related_name="aircraft_documents"
    )
    
    # Validity and expiration
    issue_date = models.DateField(null=True, blank=True)
    expiration_date = models.DateField(null=True, blank=True)
    
    # Regulatory information
    issuing_authority = models.CharField(max_length=100, blank=True, null=True)
    document_number = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['aircraft', 'document_type']),
            models.Index(fields=['expiration_date']),
        ]
    
    def __str__(self):
        return f"{self.aircraft.tail_number} - {self.title}"
    
    @property
    def is_expired(self):
        """Check if document is expired."""
        if not self.expiration_date:
            return False
        
        from django.utils import timezone
        return self.expiration_date < timezone.now().date()
    
    @property
    def days_until_expiration(self):
        """Calculate days until document expires."""
        if not self.expiration_date:
            return None
        
        from django.utils import timezone
        delta = self.expiration_date - timezone.now().date()
        return delta.days
