from django.db import models
from common.models import BaseModel
from django.utils import timezone
import uuid
from decimal import Decimal


class Transaction(BaseModel):
    """Transaction model for financial operations."""
    
    PAYMENT_METHODS = [
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('ach', 'ACH Transfer'),
        ('wire', 'Wire Transfer'),
        ('check', 'Check'),
        ('cash', 'Cash'),
        ('other', 'Other'),
    ]
    
    PAYMENT_STATUS = [
        ('created', 'Created'),
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    
    TRANSACTION_TYPES = [
        ('payment', 'Payment'),
        ('refund', 'Refund'),
        ('fee', 'Fee'),
        ('adjustment', 'Adjustment'),
    ]
    
    # Transaction identification
    key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES, default='payment')
    
    # Financial details
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    
    # Payment information
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='created')
    payment_date = models.DateTimeField(default=timezone.now)
    
    # Customer information
    email = models.EmailField()
    customer_name = models.CharField(max_length=255, blank=True, null=True)
    billing_address = models.JSONField(default=dict, blank=True)
    
    # Payment processor details
    processor_transaction_id = models.CharField(max_length=255, blank=True, null=True)
    processor_name = models.CharField(max_length=50, blank=True, null=True)  # Stripe, PayPal, etc.
    processor_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Related entities
    related_quote_id = models.UUIDField(null=True, blank=True)
    related_trip_id = models.UUIDField(null=True, blank=True)
    
    # Additional metadata
    description = models.TextField(blank=True, null=True)
    reference_number = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['key']),
            models.Index(fields=['payment_status', 'payment_date']),
            models.Index(fields=['email']),
            models.Index(fields=['related_quote_id']),
            models.Index(fields=['processor_transaction_id']),
        ]
        ordering = ['-payment_date']
    
    def __str__(self):
        return f"Transaction {self.key} - ${self.amount} - {self.payment_status}"
    
    @property
    def net_amount(self):
        """Calculate net amount after processor fees."""
        if self.processor_fee:
            return self.amount - self.processor_fee
        return self.amount
    
    @property
    def is_successful(self):
        """Check if transaction was successful."""
        return self.payment_status == 'completed'
    
    @property
    def can_be_refunded(self):
        """Check if transaction can be refunded."""
        return self.payment_status == 'completed' and self.transaction_type == 'payment'


class Invoice(BaseModel):
    """Invoice model for billing operations."""
    
    INVOICE_STATUS = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('viewed', 'Viewed'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Invoice identification
    invoice_number = models.CharField(max_length=50, unique=True, db_index=True)
    
    # Customer information
    customer_email = models.EmailField()
    customer_name = models.CharField(max_length=255)
    billing_address = models.JSONField(default=dict, blank=True)
    
    # Financial details
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    
    # Dates
    issue_date = models.DateField(default=timezone.now)
    due_date = models.DateField()
    paid_date = models.DateField(null=True, blank=True)
    
    # Status and tracking
    status = models.CharField(max_length=20, choices=INVOICE_STATUS, default='draft')
    sent_date = models.DateTimeField(null=True, blank=True)
    
    # Related entities
    related_quote_id = models.UUIDField(null=True, blank=True)
    related_trip_id = models.UUIDField(null=True, blank=True)
    
    # Payment tracking
    transactions = models.ManyToManyField(Transaction, related_name="invoices", blank=True)
    
    # Additional information
    description = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['invoice_number']),
            models.Index(fields=['status', 'due_date']),
            models.Index(fields=['customer_email']),
            models.Index(fields=['related_quote_id']),
        ]
        ordering = ['-issue_date']
    
    def __str__(self):
        return f"Invoice {self.invoice_number} - ${self.total_amount} - {self.status}"
    
    @property
    def is_overdue(self):
        """Check if invoice is overdue."""
        if self.status == 'paid':
            return False
        return timezone.now().date() > self.due_date
    
    @property
    def days_overdue(self):
        """Calculate days overdue."""
        if not self.is_overdue:
            return 0
        return (timezone.now().date() - self.due_date).days
    
    @property
    def amount_paid(self):
        """Calculate total amount paid through transactions."""
        return sum(
            t.amount for t in self.transactions.filter(
                payment_status='completed',
                transaction_type='payment'
            )
        )
    
    @property
    def amount_remaining(self):
        """Calculate remaining amount to be paid."""
        return self.total_amount - self.amount_paid


class InvoiceLineItem(BaseModel):
    """Line items for invoices."""
    
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="line_items")
    
    # Item details
    description = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('1.00'))
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Tax information
    taxable = models.BooleanField(default=True)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=4, default=Decimal('0.0000'))
    
    class Meta:
        indexes = [
            models.Index(fields=['invoice']),
        ]
    
    def __str__(self):
        return f"{self.description} - ${self.total_price}"
    
    def save(self, *args, **kwargs):
        """Calculate total price on save."""
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)


class PaymentMethod(BaseModel):
    """Stored payment methods for customers."""
    
    PAYMENT_TYPES = [
        ('credit_card', 'Credit Card'),
        ('bank_account', 'Bank Account'),
    ]
    
    # Customer information
    customer_email = models.EmailField()
    customer_name = models.CharField(max_length=255, blank=True, null=True)
    
    # Payment method details
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES)
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # Masked details for display
    last_four_digits = models.CharField(max_length=4, blank=True, null=True)
    brand = models.CharField(max_length=50, blank=True, null=True)  # Visa, MasterCard, etc.
    expiry_month = models.IntegerField(null=True, blank=True)
    expiry_year = models.IntegerField(null=True, blank=True)
    
    # Processor information
    processor_payment_method_id = models.CharField(max_length=255, blank=True, null=True)
    processor_name = models.CharField(max_length=50, blank=True, null=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['customer_email', 'is_active']),
            models.Index(fields=['processor_payment_method_id']),
        ]
    
    def __str__(self):
        if self.last_four_digits:
            return f"{self.brand} ending in {self.last_four_digits}"
        return f"{self.get_payment_type_display()} for {self.customer_email}"
    
    @property
    def is_expired(self):
        """Check if payment method is expired (for cards)."""
        if self.payment_type != 'credit_card' or not self.expiry_month or not self.expiry_year:
            return False
        
        from datetime import date
        today = date.today()
        return (self.expiry_year < today.year or 
                (self.expiry_year == today.year and self.expiry_month < today.month))
