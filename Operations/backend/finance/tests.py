from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
from .models import Transaction, Invoice, InvoiceLineItem, PaymentMethod
from .services.finance_service import TransactionService, InvoiceService, PaymentMethodService
import uuid


class TransactionModelTest(TestCase):
    """Test cases for Transaction model."""
    
    def test_transaction_creation(self):
        """Test transaction creation with required fields."""
        transaction = Transaction.objects.create(
            amount=Decimal('100.00'),
            currency='USD',
            payment_method='credit_card',
            email='customer@example.com',
            customer_name='John Doe'
        )
        
        self.assertEqual(transaction.amount, Decimal('100.00'))
        self.assertEqual(transaction.currency, 'USD')
        self.assertEqual(transaction.payment_method, 'credit_card')
        self.assertEqual(transaction.email, 'customer@example.com')
        self.assertEqual(transaction.payment_status, 'created')
        self.assertIsNotNone(transaction.key)
    
    def test_net_amount_calculation(self):
        """Test net amount calculation with processor fee."""
        transaction = Transaction.objects.create(
            amount=Decimal('100.00'),
            currency='USD',
            payment_method='credit_card',
            email='test@example.com',
            processor_fee=Decimal('3.50')
        )
        
        self.assertEqual(transaction.net_amount, Decimal('96.50'))
    
    def test_transaction_status_properties(self):
        """Test transaction status properties."""
        transaction = Transaction.objects.create(
            amount=Decimal('100.00'),
            currency='USD',
            payment_method='credit_card',
            email='test@example.com',
            payment_status='completed',
            transaction_type='payment'
        )
        
        self.assertTrue(transaction.is_successful)
        self.assertTrue(transaction.can_be_refunded)
        
        # Test refund transaction
        refund = Transaction.objects.create(
            amount=Decimal('50.00'),
            currency='USD',
            payment_method='credit_card',
            email='test@example.com',
            payment_status='completed',
            transaction_type='refund'
        )
        
        self.assertTrue(refund.is_successful)
        self.assertFalse(refund.can_be_refunded)  # Refunds can't be refunded


class InvoiceModelTest(TestCase):
    """Test cases for Invoice model."""
    
    def test_invoice_creation(self):
        """Test invoice creation with required fields."""
        due_date = timezone.now().date() + timezone.timedelta(days=30)
        
        invoice = Invoice.objects.create(
            invoice_number='INV-20240101-0001',
            customer_email='customer@example.com',
            customer_name='John Doe',
            subtotal=Decimal('100.00'),
            tax_amount=Decimal('8.00'),
            total_amount=Decimal('108.00'),
            due_date=due_date
        )
        
        self.assertEqual(invoice.invoice_number, 'INV-20240101-0001')
        self.assertEqual(invoice.customer_email, 'customer@example.com')
        self.assertEqual(invoice.total_amount, Decimal('108.00'))
        self.assertEqual(invoice.status, 'draft')
        self.assertFalse(invoice.is_overdue)
    
    def test_invoice_overdue_logic(self):
        """Test invoice overdue calculation."""
        past_due_date = timezone.now().date() - timezone.timedelta(days=5)
        
        invoice = Invoice.objects.create(
            invoice_number='INV-OVERDUE-001',
            customer_email='overdue@example.com',
            customer_name='Overdue Customer',
            subtotal=Decimal('200.00'),
            total_amount=Decimal('200.00'),
            due_date=past_due_date,
            status='sent'
        )
        
        self.assertTrue(invoice.is_overdue)
        self.assertEqual(invoice.days_overdue, 5)
    
    def test_invoice_payment_tracking(self):
        """Test invoice payment amount tracking."""
        invoice = Invoice.objects.create(
            invoice_number='INV-PAYMENT-001',
            customer_email='payment@example.com',
            customer_name='Payment Customer',
            subtotal=Decimal('500.00'),
            total_amount=Decimal('500.00'),
            due_date=timezone.now().date() + timezone.timedelta(days=30)
        )
        
        # Create completed transaction
        transaction = Transaction.objects.create(
            amount=Decimal('300.00'),
            currency='USD',
            payment_method='credit_card',
            email='payment@example.com',
            payment_status='completed',
            transaction_type='payment'
        )
        
        # Add transaction to invoice
        invoice.transactions.add(transaction)
        
        self.assertEqual(invoice.amount_paid, Decimal('300.00'))
        self.assertEqual(invoice.amount_remaining, Decimal('200.00'))


class InvoiceLineItemTest(TestCase):
    """Test cases for InvoiceLineItem model."""
    
    def setUp(self):
        self.invoice = Invoice.objects.create(
            invoice_number='INV-LINE-001',
            customer_email='line@example.com',
            customer_name='Line Customer',
            subtotal=Decimal('100.00'),
            total_amount=Decimal('100.00'),
            due_date=timezone.now().date() + timezone.timedelta(days=30)
        )
    
    def test_line_item_creation(self):
        """Test line item creation and total calculation."""
        line_item = InvoiceLineItem.objects.create(
            invoice=self.invoice,
            description='Test Service',
            quantity=Decimal('2.00'),
            unit_price=Decimal('50.00'),
            taxable=True,
            tax_rate=Decimal('0.08')
        )
        
        self.assertEqual(line_item.description, 'Test Service')
        self.assertEqual(line_item.quantity, Decimal('2.00'))
        self.assertEqual(line_item.unit_price, Decimal('50.00'))
        self.assertEqual(line_item.total_price, Decimal('100.00'))
        self.assertTrue(line_item.taxable)


class PaymentMethodModelTest(TestCase):
    """Test cases for PaymentMethod model."""
    
    def test_payment_method_creation(self):
        """Test payment method creation."""
        payment_method = PaymentMethod.objects.create(
            customer_email='payment@example.com',
            customer_name='Payment Customer',
            payment_type='credit_card',
            processor_payment_method_id='pm_test123',
            processor_name='stripe',
            last_four_digits='4242',
            brand='Visa',
            expiry_month=12,
            expiry_year=2025,
            is_default=True
        )
        
        self.assertEqual(payment_method.customer_email, 'payment@example.com')
        self.assertEqual(payment_method.payment_type, 'credit_card')
        self.assertEqual(payment_method.brand, 'Visa')
        self.assertTrue(payment_method.is_default)
        self.assertTrue(payment_method.is_active)
        self.assertFalse(payment_method.is_expired)
    
    def test_payment_method_expiration(self):
        """Test payment method expiration logic."""
        from datetime import date
        current_year = date.today().year
        
        expired_method = PaymentMethod.objects.create(
            customer_email='expired@example.com',
            payment_type='credit_card',
            processor_payment_method_id='pm_expired',
            processor_name='stripe',
            expiry_month=1,
            expiry_year=current_year - 1  # Last year
        )
        
        self.assertTrue(expired_method.is_expired)


class TransactionServiceTest(TestCase):
    """Test cases for TransactionService."""
    
    def test_create_transaction(self):
        """Test transaction creation via service."""
        transaction = TransactionService.create_transaction(
            amount=Decimal('150.00'),
            currency='USD',
            payment_method='credit_card',
            email='service@example.com',
            customer_name='Service Customer',
            description='Service test transaction'
        )
        
        self.assertIsNotNone(transaction)
        self.assertEqual(transaction.amount, Decimal('150.00'))
        self.assertEqual(transaction.email, 'service@example.com')
        self.assertEqual(transaction.payment_status, 'created')
    
    def test_process_payment(self):
        """Test payment processing via service."""
        transaction = TransactionService.create_transaction(
            amount=Decimal('100.00'),
            currency='USD',
            payment_method='credit_card',
            email='process@example.com'
        )
        
        processed = TransactionService.process_payment(
            transaction_id=transaction.id,
            processor_transaction_id='txn_test123',
            processor_name='stripe',
            processor_fee=Decimal('3.20')
        )
        
        self.assertIsNotNone(processed)
        self.assertEqual(processed.payment_status, 'processing')
        self.assertEqual(processed.processor_transaction_id, 'txn_test123')
        self.assertEqual(processed.processor_fee, Decimal('3.20'))
    
    def test_complete_payment(self):
        """Test payment completion via service."""
        transaction = TransactionService.create_transaction(
            amount=Decimal('75.00'),
            currency='USD',
            payment_method='ach',
            email='complete@example.com'
        )
        
        completed = TransactionService.complete_payment(transaction.id)
        
        self.assertIsNotNone(completed)
        self.assertEqual(completed.payment_status, 'completed')
        self.assertIsNotNone(completed.payment_date)
    
    def test_create_refund(self):
        """Test refund creation via service."""
        # Create original transaction
        original = TransactionService.create_transaction(
            amount=Decimal('200.00'),
            currency='USD',
            payment_method='credit_card',
            email='refund@example.com'
        )
        
        # Complete it first
        TransactionService.complete_payment(original.id)
        
        # Create refund
        refund = TransactionService.create_refund(
            original_transaction_id=original.id,
            refund_amount=Decimal('100.00'),
            reason='Customer request'
        )
        
        self.assertIsNotNone(refund)
        self.assertEqual(refund.transaction_type, 'refund')
        self.assertEqual(refund.amount, Decimal('100.00'))
        self.assertEqual(refund.payment_status, 'completed')
        self.assertEqual(refund.notes, 'Customer request')


class InvoiceServiceTest(TestCase):
    """Test cases for InvoiceService."""
    
    def test_create_invoice(self):
        """Test invoice creation via service."""
        line_items = [
            {
                'description': 'Flight Service',
                'quantity': Decimal('1.00'),
                'unit_price': Decimal('1000.00'),
                'total_price': Decimal('1000.00'),
                'taxable': True
            },
            {
                'description': 'Ground Transport',
                'quantity': Decimal('2.00'),
                'unit_price': Decimal('50.00'),
                'total_price': Decimal('100.00'),
                'taxable': False
            }
        ]
        
        invoice = InvoiceService.create_invoice(
            customer_email='invoice@example.com',
            customer_name='Invoice Customer',
            line_items=line_items,
            due_days=30,
            tax_rate=Decimal('0.08')
        )
        
        self.assertIsNotNone(invoice)
        self.assertEqual(invoice.customer_email, 'invoice@example.com')
        self.assertEqual(invoice.subtotal, Decimal('1100.00'))
        self.assertEqual(invoice.tax_amount, Decimal('80.00'))  # Only taxable items
        self.assertEqual(invoice.total_amount, Decimal('1180.00'))
        self.assertEqual(invoice.line_items.count(), 2)
    
    def test_send_invoice(self):
        """Test invoice sending via service."""
        line_items = [{'description': 'Test', 'unit_price': Decimal('100.00'), 'total_price': Decimal('100.00')}]
        
        invoice = InvoiceService.create_invoice(
            customer_email='send@example.com',
            customer_name='Send Customer',
            line_items=line_items
        )
        
        sent_invoice = InvoiceService.send_invoice(invoice.id)
        
        self.assertIsNotNone(sent_invoice)
        self.assertEqual(sent_invoice.status, 'sent')
        self.assertIsNotNone(sent_invoice.sent_date)
    
    def test_record_payment(self):
        """Test payment recording via service."""
        line_items = [{'description': 'Test', 'unit_price': Decimal('500.00'), 'total_price': Decimal('500.00')}]
        
        invoice = InvoiceService.create_invoice(
            customer_email='payment@example.com',
            customer_name='Payment Customer',
            line_items=line_items
        )
        
        # Create completed transaction
        transaction = TransactionService.create_transaction(
            amount=Decimal('500.00'),
            currency='USD',
            payment_method='credit_card',
            email='payment@example.com'
        )
        TransactionService.complete_payment(transaction.id)
        
        # Record payment
        updated_invoice = InvoiceService.record_payment(invoice.id, transaction.id)
        
        self.assertIsNotNone(updated_invoice)
        self.assertEqual(updated_invoice.status, 'paid')
        self.assertIsNotNone(updated_invoice.paid_date)
        self.assertTrue(updated_invoice.transactions.filter(id=transaction.id).exists())


class PaymentMethodServiceTest(TestCase):
    """Test cases for PaymentMethodService."""
    
    def test_create_payment_method(self):
        """Test payment method creation via service."""
        payment_method = PaymentMethodService.create_payment_method(
            customer_email='method@example.com',
            customer_name='Method Customer',
            payment_type='credit_card',
            processor_payment_method_id='pm_service123',
            processor_name='stripe',
            last_four_digits='1234',
            brand='MasterCard',
            expiry_month=6,
            expiry_year=2026,
            is_default=True
        )
        
        self.assertIsNotNone(payment_method)
        self.assertEqual(payment_method.customer_email, 'method@example.com')
        self.assertEqual(payment_method.brand, 'MasterCard')
        self.assertTrue(payment_method.is_default)
        self.assertTrue(payment_method.is_active)
    
    def test_set_default_payment_method(self):
        """Test setting default payment method via service."""
        # Create first payment method as default
        method1 = PaymentMethodService.create_payment_method(
            customer_email='default@example.com',
            payment_type='credit_card',
            processor_payment_method_id='pm_first',
            processor_name='stripe',
            is_default=True
        )
        
        # Create second payment method
        method2 = PaymentMethodService.create_payment_method(
            customer_email='default@example.com',
            payment_type='credit_card',
            processor_payment_method_id='pm_second',
            processor_name='stripe',
            is_default=False
        )
        
        # Set second as default
        updated_method = PaymentMethodService.set_default_payment_method(method2.id)
        
        self.assertIsNotNone(updated_method)
        self.assertTrue(updated_method.is_default)
        
        # Check first method is no longer default
        method1.refresh_from_db()
        self.assertFalse(method1.is_default)
    
    def test_get_customer_payment_methods(self):
        """Test retrieving customer payment methods."""
        customer_email = 'multi@example.com'
        
        # Create multiple payment methods
        PaymentMethodService.create_payment_method(
            customer_email=customer_email,
            payment_type='credit_card',
            processor_payment_method_id='pm_1',
            processor_name='stripe',
            is_default=True
        )
        
        PaymentMethodService.create_payment_method(
            customer_email=customer_email,
            payment_type='bank_account',
            processor_payment_method_id='pm_2',
            processor_name='stripe'
        )
        
        methods = PaymentMethodService.get_customer_payment_methods(customer_email)
        
        self.assertEqual(methods.count(), 2)
        # Default should be first
        self.assertTrue(methods.first().is_default)
    
    def test_deactivate_payment_method(self):
        """Test payment method deactivation via service."""
        payment_method = PaymentMethodService.create_payment_method(
            customer_email='deactivate@example.com',
            payment_type='credit_card',
            processor_payment_method_id='pm_deactivate',
            processor_name='stripe',
            is_default=True
        )
        
        deactivated = PaymentMethodService.deactivate_payment_method(payment_method.id)
        
        self.assertIsNotNone(deactivated)
        self.assertFalse(deactivated.is_active)
        self.assertFalse(deactivated.is_default)
