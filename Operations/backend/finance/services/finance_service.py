from django.utils import timezone
from django.db import transaction
from decimal import Decimal
from ..models import Transaction, Invoice, InvoiceLineItem, PaymentMethod
import uuid
import logging

logger = logging.getLogger(__name__)


class TransactionService:
    """Service for transaction management operations."""
    
    @staticmethod
    def create_transaction(amount, currency, payment_method, email, customer_name=None,
                          transaction_type='payment', description=None, related_quote_id=None,
                          related_trip_id=None, billing_address=None):
        """Create a new transaction."""
        try:
            transaction_obj = Transaction.objects.create(
                amount=amount,
                currency=currency,
                payment_method=payment_method,
                email=email,
                customer_name=customer_name,
                transaction_type=transaction_type,
                description=description,
                related_quote_id=related_quote_id,
                related_trip_id=related_trip_id,
                billing_address=billing_address or {},
                payment_status='created'
            )
            
            logger.info(f"Transaction created: {transaction_obj.key} - ${amount}")
            return transaction_obj
            
        except Exception as e:
            logger.error(f"Error creating transaction: {str(e)}")
            raise
    
    @staticmethod
    def process_payment(transaction_id, processor_transaction_id, processor_name, 
                       processor_fee=None):
        """Process a payment transaction."""
        try:
            with transaction.atomic():
                trans = Transaction.objects.select_for_update().get(id=transaction_id)
                
                if trans.payment_status != 'created':
                    logger.error(f"Transaction not in processable state: {trans.payment_status}")
                    return None
                
                trans.payment_status = 'processing'
                trans.processor_transaction_id = processor_transaction_id
                trans.processor_name = processor_name
                trans.processor_fee = processor_fee
                trans.save()
                
                logger.info(f"Transaction processing: {trans.key}")
                return trans
                
        except Transaction.DoesNotExist:
            logger.error(f"Transaction not found: {transaction_id}")
            return None
        except Exception as e:
            logger.error(f"Error processing payment: {str(e)}")
            raise
    
    @staticmethod
    def complete_payment(transaction_id):
        """Mark a payment as completed."""
        try:
            trans = Transaction.objects.get(id=transaction_id)
            trans.payment_status = 'completed'
            trans.payment_date = timezone.now()
            trans.save()
            
            logger.info(f"Transaction completed: {trans.key}")
            return trans
            
        except Transaction.DoesNotExist:
            logger.error(f"Transaction not found: {transaction_id}")
            return None
    
    @staticmethod
    def fail_payment(transaction_id, reason=None):
        """Mark a payment as failed."""
        try:
            trans = Transaction.objects.get(id=transaction_id)
            trans.payment_status = 'failed'
            if reason:
                trans.notes = reason
            trans.save()
            
            logger.info(f"Transaction failed: {trans.key}")
            return trans
            
        except Transaction.DoesNotExist:
            logger.error(f"Transaction not found: {transaction_id}")
            return None
    
    @staticmethod
    def create_refund(original_transaction_id, refund_amount=None, reason=None):
        """Create a refund transaction."""
        try:
            original = Transaction.objects.get(id=original_transaction_id)
            
            if not original.can_be_refunded:
                logger.error(f"Transaction cannot be refunded: {original.key}")
                return None
            
            refund_amount = refund_amount or original.amount
            
            refund = Transaction.objects.create(
                amount=refund_amount,
                currency=original.currency,
                payment_method=original.payment_method,
                email=original.email,
                customer_name=original.customer_name,
                transaction_type='refund',
                description=f"Refund for transaction {original.key}",
                related_quote_id=original.related_quote_id,
                related_trip_id=original.related_trip_id,
                billing_address=original.billing_address,
                payment_status='completed',
                notes=reason
            )
            
            logger.info(f"Refund created: {refund.key} for ${refund_amount}")
            return refund
            
        except Transaction.DoesNotExist:
            logger.error(f"Original transaction not found: {original_transaction_id}")
            return None
        except Exception as e:
            logger.error(f"Error creating refund: {str(e)}")
            raise


class InvoiceService:
    """Service for invoice management operations."""
    
    @staticmethod
    def create_invoice(customer_email, customer_name, line_items, due_days=30,
                      related_quote_id=None, related_trip_id=None, billing_address=None,
                      description=None, tax_rate=Decimal('0.00')):
        """Create a new invoice with line items."""
        try:
            with transaction.atomic():
                # Generate invoice number
                invoice_number = InvoiceService._generate_invoice_number()
                
                # Calculate totals
                subtotal = sum(item['total_price'] for item in line_items)
                tax_amount = subtotal * tax_rate
                total_amount = subtotal + tax_amount
                
                # Calculate due date
                due_date = timezone.now().date() + timezone.timedelta(days=due_days)
                
                # Create invoice
                invoice = Invoice.objects.create(
                    invoice_number=invoice_number,
                    customer_email=customer_email,
                    customer_name=customer_name,
                    billing_address=billing_address or {},
                    subtotal=subtotal,
                    tax_amount=tax_amount,
                    total_amount=total_amount,
                    due_date=due_date,
                    related_quote_id=related_quote_id,
                    related_trip_id=related_trip_id,
                    description=description,
                    status='draft'
                )
                
                # Create line items
                for item_data in line_items:
                    InvoiceLineItem.objects.create(
                        invoice=invoice,
                        description=item_data['description'],
                        quantity=item_data.get('quantity', Decimal('1.00')),
                        unit_price=item_data['unit_price'],
                        total_price=item_data['total_price'],
                        taxable=item_data.get('taxable', True),
                        tax_rate=tax_rate if item_data.get('taxable', True) else Decimal('0.00')
                    )
                
                logger.info(f"Invoice created: {invoice.invoice_number} - ${total_amount}")
                return invoice
                
        except Exception as e:
            logger.error(f"Error creating invoice: {str(e)}")
            raise
    
    @staticmethod
    def _generate_invoice_number():
        """Generate a unique invoice number."""
        timestamp = timezone.now().strftime('%Y%m%d')
        count = Invoice.objects.filter(
            invoice_number__startswith=f"INV-{timestamp}"
        ).count() + 1
        return f"INV-{timestamp}-{count:04d}"
    
    @staticmethod
    def send_invoice(invoice_id):
        """Mark invoice as sent."""
        try:
            invoice = Invoice.objects.get(id=invoice_id)
            invoice.status = 'sent'
            invoice.sent_date = timezone.now()
            invoice.save()
            
            logger.info(f"Invoice sent: {invoice.invoice_number}")
            return invoice
            
        except Invoice.DoesNotExist:
            logger.error(f"Invoice not found: {invoice_id}")
            return None
    
    @staticmethod
    def record_payment(invoice_id, transaction_id):
        """Record a payment against an invoice."""
        try:
            with transaction.atomic():
                invoice = Invoice.objects.get(id=invoice_id)
                trans = Transaction.objects.get(id=transaction_id)
                
                if trans.payment_status != 'completed':
                    logger.error(f"Cannot record incomplete payment: {trans.key}")
                    return None
                
                # Add transaction to invoice
                invoice.transactions.add(trans)
                
                # Update invoice status based on payment
                if invoice.amount_paid >= invoice.total_amount:
                    invoice.status = 'paid'
                    invoice.paid_date = timezone.now().date()
                
                invoice.save()
                
                logger.info(f"Payment recorded for invoice: {invoice.invoice_number}")
                return invoice
                
        except (Invoice.DoesNotExist, Transaction.DoesNotExist) as e:
            logger.error(f"Invoice or transaction not found: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error recording payment: {str(e)}")
            raise
    
    @staticmethod
    def get_overdue_invoices():
        """Get all overdue invoices."""
        try:
            today = timezone.now().date()
            return Invoice.objects.filter(
                due_date__lt=today,
                status__in=['sent', 'viewed']
            ).order_by('due_date')
        except Exception as e:
            logger.error(f"Error getting overdue invoices: {str(e)}")
            return Invoice.objects.none()
    
    @staticmethod
    def cancel_invoice(invoice_id, reason=None):
        """Cancel an invoice."""
        try:
            invoice = Invoice.objects.get(id=invoice_id)
            
            if invoice.status == 'paid':
                logger.error(f"Cannot cancel paid invoice: {invoice.invoice_number}")
                return None
            
            invoice.status = 'cancelled'
            if reason:
                invoice.notes = reason
            invoice.save()
            
            logger.info(f"Invoice cancelled: {invoice.invoice_number}")
            return invoice
            
        except Invoice.DoesNotExist:
            logger.error(f"Invoice not found: {invoice_id}")
            return None


class PaymentMethodService:
    """Service for payment method management."""
    
    @staticmethod
    def create_payment_method(customer_email, payment_type, processor_payment_method_id,
                             processor_name, customer_name=None, last_four_digits=None,
                             brand=None, expiry_month=None, expiry_year=None, is_default=False):
        """Create a new payment method."""
        try:
            with transaction.atomic():
                # If this is set as default, unset other defaults for this customer
                if is_default:
                    PaymentMethod.objects.filter(
                        customer_email=customer_email,
                        is_default=True
                    ).update(is_default=False)
                
                payment_method = PaymentMethod.objects.create(
                    customer_email=customer_email,
                    customer_name=customer_name,
                    payment_type=payment_type,
                    processor_payment_method_id=processor_payment_method_id,
                    processor_name=processor_name,
                    last_four_digits=last_four_digits,
                    brand=brand,
                    expiry_month=expiry_month,
                    expiry_year=expiry_year,
                    is_default=is_default,
                    is_active=True
                )
                
                logger.info(f"Payment method created for {customer_email}")
                return payment_method
                
        except Exception as e:
            logger.error(f"Error creating payment method: {str(e)}")
            raise
    
    @staticmethod
    def get_customer_payment_methods(customer_email, active_only=True):
        """Get payment methods for a customer."""
        try:
            queryset = PaymentMethod.objects.filter(customer_email=customer_email)
            if active_only:
                queryset = queryset.filter(is_active=True)
            return queryset.order_by('-is_default', '-created_on')
        except Exception as e:
            logger.error(f"Error getting payment methods: {str(e)}")
            return PaymentMethod.objects.none()
    
    @staticmethod
    def set_default_payment_method(payment_method_id):
        """Set a payment method as default for the customer."""
        try:
            with transaction.atomic():
                payment_method = PaymentMethod.objects.get(id=payment_method_id)
                
                # Unset other defaults for this customer
                PaymentMethod.objects.filter(
                    customer_email=payment_method.customer_email,
                    is_default=True
                ).update(is_default=False)
                
                # Set this one as default
                payment_method.is_default = True
                payment_method.save()
                
                logger.info(f"Default payment method set for {payment_method.customer_email}")
                return payment_method
                
        except PaymentMethod.DoesNotExist:
            logger.error(f"Payment method not found: {payment_method_id}")
            return None
        except Exception as e:
            logger.error(f"Error setting default payment method: {str(e)}")
            raise
    
    @staticmethod
    def deactivate_payment_method(payment_method_id):
        """Deactivate a payment method."""
        try:
            payment_method = PaymentMethod.objects.get(id=payment_method_id)
            payment_method.is_active = False
            payment_method.is_default = False
            payment_method.save()
            
            logger.info(f"Payment method deactivated: {payment_method_id}")
            return payment_method
            
        except PaymentMethod.DoesNotExist:
            logger.error(f"Payment method not found: {payment_method_id}")
            return None
