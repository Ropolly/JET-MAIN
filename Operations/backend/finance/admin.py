from django.contrib import admin
from .models import Transaction, Invoice, InvoiceLineItem, PaymentMethod


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """Admin configuration for Transaction model."""
    list_display = [
        'key', 'transaction_type', 'amount', 'currency', 'payment_status',
        'payment_method', 'email', 'payment_date'
    ]
    list_filter = [
        'transaction_type', 'payment_status', 'payment_method', 
        'currency', 'payment_date', 'processor_name'
    ]
    search_fields = [
        'key', 'email', 'customer_name', 'processor_transaction_id',
        'reference_number', 'description'
    ]
    readonly_fields = [
        'id', 'key', 'net_amount', 'is_successful', 'can_be_refunded',
        'created_on', 'updated_on'
    ]
    
    fieldsets = (
        ('Transaction Details', {
            'fields': (
                'key', 'transaction_type', 'amount', 'currency', 'net_amount'
            )
        }),
        ('Payment Information', {
            'fields': (
                'payment_method', 'payment_status', 'payment_date'
            )
        }),
        ('Customer Information', {
            'fields': (
                'email', 'customer_name', 'billing_address'
            )
        }),
        ('Processor Details', {
            'fields': (
                'processor_transaction_id', 'processor_name', 'processor_fee'
            ),
            'classes': ('collapse',)
        }),
        ('Related Entities', {
            'fields': (
                'related_quote_id', 'related_trip_id'
            )
        }),
        ('Additional Information', {
            'fields': (
                'description', 'reference_number', 'notes'
            ),
            'classes': ('collapse',)
        }),
        ('Status Flags', {
            'fields': (
                'is_successful', 'can_be_refunded'
            ),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_on', 'updated_on'),
            'classes': ('collapse',)
        }),
    )
    
    def net_amount(self, obj):
        """Display net amount after fees."""
        return f"${obj.net_amount:.2f}"
    net_amount.short_description = 'Net Amount'


class InvoiceLineItemInline(admin.TabularInline):
    """Inline admin for invoice line items."""
    model = InvoiceLineItem
    extra = 1
    readonly_fields = ['total_price']


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    """Admin configuration for Invoice model."""
    list_display = [
        'invoice_number', 'customer_email', 'total_amount', 'status',
        'issue_date', 'due_date', 'is_overdue', 'amount_paid'
    ]
    list_filter = [
        'status', 'currency', 'issue_date', 'due_date', 'paid_date'
    ]
    search_fields = [
        'invoice_number', 'customer_email', 'customer_name', 'description'
    ]
    readonly_fields = [
        'id', 'invoice_number', 'is_overdue', 'days_overdue',
        'amount_paid', 'amount_remaining', 'created_on', 'updated_on'
    ]
    inlines = [InvoiceLineItemInline]
    
    fieldsets = (
        ('Invoice Information', {
            'fields': (
                'invoice_number', 'status', 'issue_date', 'due_date', 'paid_date'
            )
        }),
        ('Customer Information', {
            'fields': (
                'customer_email', 'customer_name', 'billing_address'
            )
        }),
        ('Financial Details', {
            'fields': (
                'subtotal', 'tax_amount', 'total_amount', 'currency',
                'amount_paid', 'amount_remaining'
            )
        }),
        ('Status Information', {
            'fields': (
                'sent_date', 'is_overdue', 'days_overdue'
            ),
            'classes': ('collapse',)
        }),
        ('Related Entities', {
            'fields': (
                'related_quote_id', 'related_trip_id'
            )
        }),
        ('Additional Information', {
            'fields': (
                'description', 'notes'
            ),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_on', 'updated_on'),
            'classes': ('collapse',)
        }),
    )
    
    def is_overdue(self, obj):
        """Display overdue status."""
        return obj.is_overdue
    is_overdue.boolean = True
    is_overdue.short_description = 'Overdue'
    
    def amount_paid(self, obj):
        """Display amount paid."""
        return f"${obj.amount_paid:.2f}"
    amount_paid.short_description = 'Amount Paid'


@admin.register(InvoiceLineItem)
class InvoiceLineItemAdmin(admin.ModelAdmin):
    """Admin configuration for InvoiceLineItem model."""
    list_display = [
        'invoice', 'description', 'quantity', 'unit_price', 
        'total_price', 'taxable'
    ]
    list_filter = ['taxable', 'tax_rate']
    search_fields = ['description', 'invoice__invoice_number']
    readonly_fields = ['id', 'total_price', 'created_on', 'updated_on']
    
    fieldsets = (
        ('Line Item Details', {
            'fields': (
                'invoice', 'description', 'quantity', 'unit_price', 'total_price'
            )
        }),
        ('Tax Information', {
            'fields': ('taxable', 'tax_rate')
        }),
        ('Timestamps', {
            'fields': ('created_on', 'updated_on'),
            'classes': ('collapse',)
        }),
    )


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    """Admin configuration for PaymentMethod model."""
    list_display = [
        'customer_email', 'payment_type', 'brand', 'last_four_digits',
        'is_default', 'is_active', 'is_expired'
    ]
    list_filter = [
        'payment_type', 'is_default', 'is_active', 'brand',
        'processor_name', 'expiry_year'
    ]
    search_fields = [
        'customer_email', 'customer_name', 'brand', 'last_four_digits',
        'processor_payment_method_id'
    ]
    readonly_fields = [
        'id', 'is_expired', 'created_on', 'updated_on'
    ]
    
    fieldsets = (
        ('Customer Information', {
            'fields': ('customer_email', 'customer_name')
        }),
        ('Payment Method Details', {
            'fields': (
                'payment_type', 'is_default', 'is_active'
            )
        }),
        ('Card Information', {
            'fields': (
                'last_four_digits', 'brand', 'expiry_month', 
                'expiry_year', 'is_expired'
            )
        }),
        ('Processor Information', {
            'fields': (
                'processor_payment_method_id', 'processor_name'
            ),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_on', 'updated_on'),
            'classes': ('collapse',)
        }),
    )
    
    def is_expired(self, obj):
        """Display expiration status."""
        return obj.is_expired
    is_expired.boolean = True
    is_expired.short_description = 'Expired'
