from rest_framework import serializers
from decimal import Decimal
from .models import Transaction, Invoice, InvoiceLineItem, PaymentMethod


class TransactionSerializer(serializers.ModelSerializer):
    """Serializer for Transaction model."""
    net_amount = serializers.ReadOnlyField()
    is_successful = serializers.ReadOnlyField()
    can_be_refunded = serializers.ReadOnlyField()
    payment_method_display = serializers.CharField(source='get_payment_method_display', read_only=True)
    payment_status_display = serializers.CharField(source='get_payment_status_display', read_only=True)
    transaction_type_display = serializers.CharField(source='get_transaction_type_display', read_only=True)
    
    class Meta:
        model = Transaction
        fields = [
            'id', 'key', 'transaction_type', 'transaction_type_display',
            'amount', 'currency', 'net_amount', 'payment_method', 'payment_method_display',
            'payment_status', 'payment_status_display', 'payment_date',
            'email', 'customer_name', 'billing_address',
            'processor_transaction_id', 'processor_name', 'processor_fee',
            'related_quote_id', 'related_trip_id', 'description', 'reference_number',
            'notes', 'is_successful', 'can_be_refunded', 'created_on', 'updated_on'
        ]
        read_only_fields = [
            'id', 'key', 'payment_date', 'processor_transaction_id', 
            'processor_name', 'processor_fee', 'created_on', 'updated_on'
        ]
    
    def validate_amount(self, value):
        """Validate transaction amount."""
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        if value > Decimal('999999.99'):
            raise serializers.ValidationError("Amount cannot exceed $999,999.99.")
        return value
    
    def validate_email(self, value):
        """Validate customer email."""
        if not value:
            raise serializers.ValidationError("Customer email is required.")
        return value.lower().strip()


class CreateTransactionSerializer(serializers.Serializer):
    """Serializer for creating new transactions."""
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.CharField(max_length=3, default='USD')
    payment_method = serializers.ChoiceField(choices=Transaction.PAYMENT_METHODS)
    email = serializers.EmailField()
    customer_name = serializers.CharField(max_length=255, required=False)
    transaction_type = serializers.ChoiceField(choices=Transaction.TRANSACTION_TYPES, default='payment')
    description = serializers.CharField(required=False)
    related_quote_id = serializers.UUIDField(required=False)
    related_trip_id = serializers.UUIDField(required=False)
    billing_address = serializers.JSONField(required=False)
    
    def validate_amount(self, value):
        """Validate transaction amount."""
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value


class ProcessPaymentSerializer(serializers.Serializer):
    """Serializer for processing payments."""
    processor_transaction_id = serializers.CharField(max_length=255)
    processor_name = serializers.CharField(max_length=50)
    processor_fee = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)


class RefundSerializer(serializers.Serializer):
    """Serializer for creating refunds."""
    refund_amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    reason = serializers.CharField(required=False)
    
    def validate_refund_amount(self, value):
        """Validate refund amount."""
        if value and value <= 0:
            raise serializers.ValidationError("Refund amount must be greater than zero.")
        return value


class InvoiceLineItemSerializer(serializers.ModelSerializer):
    """Serializer for InvoiceLineItem model."""
    
    class Meta:
        model = InvoiceLineItem
        fields = [
            'id', 'description', 'quantity', 'unit_price', 'total_price',
            'taxable', 'tax_rate'
        ]
        read_only_fields = ['id', 'total_price']
    
    def validate_quantity(self, value):
        """Validate quantity."""
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        return value
    
    def validate_unit_price(self, value):
        """Validate unit price."""
        if value < 0:
            raise serializers.ValidationError("Unit price cannot be negative.")
        return value


class InvoiceSerializer(serializers.ModelSerializer):
    """Serializer for Invoice model."""
    line_items = InvoiceLineItemSerializer(many=True, read_only=True)
    is_overdue = serializers.ReadOnlyField()
    days_overdue = serializers.ReadOnlyField()
    amount_paid = serializers.ReadOnlyField()
    amount_remaining = serializers.ReadOnlyField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Invoice
        fields = [
            'id', 'invoice_number', 'customer_email', 'customer_name',
            'billing_address', 'subtotal', 'tax_amount', 'total_amount',
            'currency', 'issue_date', 'due_date', 'paid_date',
            'status', 'status_display', 'sent_date', 'related_quote_id',
            'related_trip_id', 'description', 'notes', 'line_items',
            'is_overdue', 'days_overdue', 'amount_paid', 'amount_remaining',
            'created_on', 'updated_on'
        ]
        read_only_fields = [
            'id', 'invoice_number', 'sent_date', 'paid_date',
            'created_on', 'updated_on'
        ]
    
    def validate_customer_email(self, value):
        """Validate customer email."""
        if not value:
            raise serializers.ValidationError("Customer email is required.")
        return value.lower().strip()
    
    def validate_due_date(self, value):
        """Validate due date."""
        from django.utils import timezone
        if value < timezone.now().date():
            raise serializers.ValidationError("Due date cannot be in the past.")
        return value


class CreateInvoiceSerializer(serializers.Serializer):
    """Serializer for creating new invoices."""
    customer_email = serializers.EmailField()
    customer_name = serializers.CharField(max_length=255)
    billing_address = serializers.JSONField(required=False)
    due_days = serializers.IntegerField(default=30, min_value=1)
    related_quote_id = serializers.UUIDField(required=False)
    related_trip_id = serializers.UUIDField(required=False)
    description = serializers.CharField(required=False)
    tax_rate = serializers.DecimalField(max_digits=5, decimal_places=4, default=Decimal('0.00'))
    line_items = serializers.ListField(
        child=serializers.DictField(),
        min_length=1
    )
    
    def validate_line_items(self, value):
        """Validate line items format."""
        required_fields = ['description', 'unit_price', 'total_price']
        
        for item in value:
            for field in required_fields:
                if field not in item:
                    raise serializers.ValidationError(f"Line item missing required field: {field}")
            
            # Validate numeric fields
            try:
                unit_price = Decimal(str(item['unit_price']))
                total_price = Decimal(str(item['total_price']))
                quantity = Decimal(str(item.get('quantity', '1.00')))
                
                if unit_price < 0:
                    raise serializers.ValidationError("Unit price cannot be negative.")
                if total_price < 0:
                    raise serializers.ValidationError("Total price cannot be negative.")
                if quantity <= 0:
                    raise serializers.ValidationError("Quantity must be greater than zero.")
                    
            except (ValueError, TypeError):
                raise serializers.ValidationError("Invalid numeric values in line items.")
        
        return value


class PaymentMethodSerializer(serializers.ModelSerializer):
    """Serializer for PaymentMethod model."""
    is_expired = serializers.ReadOnlyField()
    payment_type_display = serializers.CharField(source='get_payment_type_display', read_only=True)
    
    class Meta:
        model = PaymentMethod
        fields = [
            'id', 'customer_email', 'customer_name', 'payment_type',
            'payment_type_display', 'is_default', 'is_active',
            'last_four_digits', 'brand', 'expiry_month', 'expiry_year',
            'is_expired', 'created_on', 'updated_on'
        ]
        read_only_fields = [
            'id', 'processor_payment_method_id', 'processor_name',
            'created_on', 'updated_on'
        ]
    
    def validate_customer_email(self, value):
        """Validate customer email."""
        if not value:
            raise serializers.ValidationError("Customer email is required.")
        return value.lower().strip()
    
    def validate_expiry_month(self, value):
        """Validate expiry month."""
        if value and (value < 1 or value > 12):
            raise serializers.ValidationError("Expiry month must be between 1 and 12.")
        return value
    
    def validate_expiry_year(self, value):
        """Validate expiry year."""
        if value:
            from datetime import date
            current_year = date.today().year
            if value < current_year or value > current_year + 20:
                raise serializers.ValidationError("Invalid expiry year.")
        return value


class CreatePaymentMethodSerializer(serializers.Serializer):
    """Serializer for creating payment methods."""
    customer_email = serializers.EmailField()
    customer_name = serializers.CharField(max_length=255, required=False)
    payment_type = serializers.ChoiceField(choices=PaymentMethod.PAYMENT_TYPES)
    processor_payment_method_id = serializers.CharField(max_length=255)
    processor_name = serializers.CharField(max_length=50)
    last_four_digits = serializers.CharField(max_length=4, required=False)
    brand = serializers.CharField(max_length=50, required=False)
    expiry_month = serializers.IntegerField(min_value=1, max_value=12, required=False)
    expiry_year = serializers.IntegerField(required=False)
    is_default = serializers.BooleanField(default=False)
    
    def validate_customer_email(self, value):
        """Validate customer email."""
        return value.lower().strip()
