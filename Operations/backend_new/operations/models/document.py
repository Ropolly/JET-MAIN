from core.models import BaseModel
from django.db import models

DOCUMENT_TYPES = [
    ('gendec', 'General Declaration'),
    ('quote', 'Quote Form'),
    ('customer_itinerary', 'Customer Itinerary'),
    ('internal_itinerary', 'Internal Itinerary'),
    ('payment_agreement', 'Payment Agreement'),
    ('consent_transport', 'Consent for Transport'),
    ('psa', 'Patient Service Agreement'),
    ('handling_request', 'Handling Request'),
    ('letter_of_medical_necessity', 'Letter of Medical Necessity'),
    ('insurance_card', 'Insurance Card'),
    ]

class Document(models.Model):
    filename = models.CharField(max_length=255)
    content = models.BinaryField(null=True, blank=True)  # Making it optional since we'll use file_path
    file_path = models.CharField(max_length=500, blank=True, null=True)  # Path to file on filesystem
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPES, null=True, blank=True)
    flag = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    
    # Relationships - each document can belong to one of these
    trip = models.ForeignKey('Trip', on_delete=models.CASCADE, related_name='documents', null=True, blank=True)
    contact = models.ForeignKey('Contact', on_delete=models.CASCADE, related_name='documents', null=True, blank=True)
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, related_name='patient_documents', null=True, blank=True)
    passenger = models.ForeignKey('Passenger', on_delete=models.CASCADE, related_name='passenger_documents', null=True, blank=True)
    created_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='created_documents')
    
    def __str__(self):
        doc_type = dict(self.DOCUMENT_TYPES).get(self.document_type, 'Document')
        return f"{doc_type}: {self.filename}"
