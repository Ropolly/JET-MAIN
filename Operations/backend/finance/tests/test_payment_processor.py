"""
Django test cases for payment processing functionality.

Converted from custom test scripts to proper Django TestCase.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from unittest.mock import Mock, patch, MagicMock
from decimal import Decimal
from datetime import date, timedelta
from finance.services.payment_processor import PaymentProcessorService
from finance.services.finance_service import FinanceService, InvoiceService
from finance.models import Transaction, PaymentMethod, Invoice, LineItem
from contacts.models import Contact


class PaymentProcessorServiceTest(TestCase):
    """Test cases for PaymentProcessorService."""
    
    def setUp(self):
        """Set up test data."""
        self.service = PaymentProcessorService()
        
    @patch('stripe.PaymentIntent.create')
    def test_stripe_payment_intent_creation(self, mock_stripe_create):
        """Test Stripe payment intent creation."""
        # Mock Stripe response
        mock_intent = Mock()
        mock_intent.id = 'pi_test123'
        mock_intent.client_secret = 'pi_test123_secret'
        mock_intent.status = 'requires_payment_method'
        mock_stripe_create.return_value = mock_intent
        
        result = self.service.create_payment_intent(
            amount=Decimal('100.00'),
            currency='usd',
            provider='stripe'
        )
        
        self.assertEqual(result['payment_intent_id'], 'pi_test123')
        self.assertEqual(result['client_secret'], 'pi_test123_secret')
        self.assertEqual(result['status'], 'requires_payment_method')
        
    @patch('squareup.payments_api.PaymentsApi.create_payment')
    def test_square_payment_creation(self, mock_square_create):
        """Test Square payment creation."""
        # Mock Square response
        mock_response = Mock()
        mock_payment = Mock()
        mock_payment.id = 'sq_test123'
        mock_payment.status = 'COMPLETED'
        mock_response.body = {'payment': mock_payment}
        mock_square_create.return_value = mock_response
        
        result = self.service.process_payment(
            amount=Decimal('50.00'),
            payment_method_token='cnon:test-token',
            provider='square'
        )
        
        self.assertEqual(result['transaction_id'], 'sq_test123')
        self.assertEqual(result['status'], 'COMPLETED')
        
    def test_unsupported_provider_error(self):
        """Test error handling for unsupported payment provider."""
        with self.assertRaises(ValueError):
            self.service.create_payment_intent(
                amount=Decimal('100.00'),
                provider='unsupported_provider'
            )
            
    @patch('stripe.Refund.create')
    def test_stripe_refund_processing(self, mock_stripe_refund):
        """Test Stripe refund processing."""
        # Mock Stripe refund response
        mock_refund = Mock()
        mock_refund.id = 're_test123'
        mock_refund.status = 'succeeded'
        mock_refund.amount = 5000  # $50.00 in cents
        mock_stripe_refund.return_value = mock_refund
        
        result = self.service.process_refund(
            transaction_id='pi_original123',
            amount=Decimal('50.00'),
            provider='stripe'
        )
        
        self.assertEqual(result['refund_id'], 're_test123')
        self.assertEqual(result['status'], 'succeeded')
        self.assertEqual(result['amount'], Decimal('50.00'))
        
    def test_payment_validation(self):
        """Test payment amount and currency validation."""
        with self.assertRaises(ValueError):
            self.service.create_payment_intent(
                amount=Decimal('0.00'),  # Zero amount
                provider='stripe'
            )
            
        with self.assertRaises(ValueError):
            self.service.create_payment_intent(
                amount=Decimal('-10.00'),  # Negative amount
                provider='stripe'
            )


class FinanceServiceTest(TestCase):
    """Test cases for FinanceService business logic."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.contact = Contact.objects.create(
            first_name='John',
            last_name='Customer',
            email='john@example.com',
            phone='+1234567890'
        )
        
    def test_create_transaction_record(self):
        """Test transaction record creation."""
        transaction = FinanceService.create_transaction(
            transaction_id='txn_test123',
            amount=Decimal('250.00'),
            currency='USD',
            payment_provider='stripe',
            customer_email='john@example.com',
            description='Test flight payment'
        )
        
        self.assertEqual(transaction.transaction_id, 'txn_test123')
        self.assertEqual(transaction.amount, Decimal('250.00'))
        self.assertEqual(transaction.currency, 'USD')
        self.assertEqual(transaction.status, 'pending')
        
    def test_calculate_payment_fees(self):
        """Test payment fee calculations."""
        # Stripe fees: 2.9% + $0.30
        stripe_fee = FinanceService.calculate_payment_fees(
            amount=Decimal('100.00'),
            provider='stripe'
        )
        expected_stripe = Decimal('100.00') * Decimal('0.029') + Decimal('0.30')
        self.assertEqual(stripe_fee, expected_stripe)
        
        # Square fees: 2.6% + $0.10
        square_fee = FinanceService.calculate_payment_fees(
            amount=Decimal('100.00'),
            provider='square'
        )
        expected_square = Decimal('100.00') * Decimal('0.026') + Decimal('0.10')
        self.assertEqual(square_fee, expected_square)
        
    def test_transaction_status_updates(self):
        """Test transaction status transitions."""
        transaction = Transaction.objects.create(
            transaction_id='status_test',
            amount=Decimal('100.00'),
            currency='USD',
            status='pending'
        )
        
        # Valid transition: pending -> completed
        updated = FinanceService.update_transaction_status(
            transaction.id, 'completed'
        )
        self.assertEqual(updated.status, 'completed')
        
        # Invalid transition: completed -> pending
        with self.assertRaises(ValueError):
            FinanceService.update_transaction_status(
                transaction.id, 'pending'
            )


class InvoiceServiceTest(TestCase):
    """Test cases for InvoiceService."""
    
    def setUp(self):
        """Set up test data."""
        self.contact = Contact.objects.create(
            first_name='Jane',
            last_name='Client',
            email='jane@example.com',
            company='Test Aviation'
        )
        
    def test_create_invoice_with_line_items(self):
        """Test invoice creation with line items."""
        invoice = InvoiceService.create_invoice(
            customer=self.contact,
            invoice_number='INV-2024-001',
            due_date=date.today() + timedelta(days=30),
            line_items=[
                {
                    'description': 'Flight JFK-LAX',
                    'quantity': 1,
                    'unit_price': Decimal('15000.00')
                },
                {
                    'description': 'Ground handling',
                    'quantity': 2,
                    'unit_price': Decimal('500.00')
                }
            ]
        )
        
        self.assertEqual(invoice.customer, self.contact)
        self.assertEqual(invoice.invoice_number, 'INV-2024-001')
        self.assertEqual(invoice.status, 'draft')
        
        # Check line items
        line_items = invoice.line_items.all()
        self.assertEqual(line_items.count(), 2)
        
        # Check total calculation
        expected_total = Decimal('15000.00') + (Decimal('500.00') * 2)
        self.assertEqual(invoice.total_amount, expected_total)
        
    def test_invoice_payment_tracking(self):
        """Test invoice payment tracking."""
        invoice = Invoice.objects.create(
            customer=self.contact,
            invoice_number='PAY-TEST-001',
            total_amount=Decimal('1000.00'),
            status='sent'
        )
        
        # Record partial payment
        InvoiceService.record_payment(
            invoice_id=invoice.id,
            amount=Decimal('600.00'),
            payment_method='credit_card',
            transaction_id='txn_partial'
        )
        
        invoice.refresh_from_db()
        self.assertEqual(invoice.paid_amount, Decimal('600.00'))
        self.assertEqual(invoice.balance_due, Decimal('400.00'))
        self.assertEqual(invoice.status, 'partially_paid')
        
        # Record remaining payment
        InvoiceService.record_payment(
            invoice_id=invoice.id,
            amount=Decimal('400.00'),
            payment_method='credit_card',
            transaction_id='txn_final'
        )
        
        invoice.refresh_from_db()
        self.assertEqual(invoice.paid_amount, Decimal('1000.00'))
        self.assertEqual(invoice.balance_due, Decimal('0.00'))
        self.assertEqual(invoice.status, 'paid')
        
    def test_overdue_invoice_detection(self):
        """Test overdue invoice detection."""
        past_due_date = date.today() - timedelta(days=5)
        
        overdue_invoice = Invoice.objects.create(
            customer=self.contact,
            invoice_number='OVERDUE-001',
            total_amount=Decimal('500.00'),
            due_date=past_due_date,
            status='sent'
        )
        
        overdue_invoices = InvoiceService.get_overdue_invoices()
        self.assertIn(overdue_invoice, overdue_invoices)
        
        # Check days overdue calculation
        days_overdue = InvoiceService.calculate_days_overdue(overdue_invoice)
        self.assertEqual(days_overdue, 5)


class TransactionModelTest(TestCase):
    """Test cases for Transaction model."""
    
    def test_transaction_creation(self):
        """Test Transaction model creation."""
        transaction = Transaction.objects.create(
            transaction_id='test_txn_123',
            amount=Decimal('150.00'),
            currency='USD',
            status='completed',
            payment_provider='stripe',
            description='Test payment'
        )
        
        self.assertEqual(transaction.transaction_id, 'test_txn_123')
        self.assertEqual(transaction.amount, Decimal('150.00'))
        self.assertEqual(transaction.currency, 'USD')
        self.assertEqual(transaction.status, 'completed')
        self.assertEqual(str(transaction), 'test_txn_123 - $150.00')
        
    def test_transaction_amount_validation(self):
        """Test transaction amount validation."""
        with self.assertRaises(Exception):
            Transaction.objects.create(
                transaction_id='invalid_txn',
                amount=Decimal('-50.00'),  # Negative amount should fail
                currency='USD',
                status='pending'
            )


class PaymentMethodModelTest(TestCase):
    """Test cases for PaymentMethod model."""
    
    def test_payment_method_creation(self):
        """Test PaymentMethod model creation."""
        payment_method = PaymentMethod.objects.create(
            customer_email='test@example.com',
            provider='stripe',
            provider_payment_method_id='pm_test123',
            payment_type='card',
            last_four_digits='4242',
            expiry_month=12,
            expiry_year=2025
        )
        
        self.assertEqual(payment_method.customer_email, 'test@example.com')
        self.assertEqual(payment_method.provider, 'stripe')
        self.assertEqual(payment_method.last_four_digits, '4242')
        self.assertTrue(payment_method.is_active)
        
    def test_payment_method_masking(self):
        """Test payment method number masking."""
        payment_method = PaymentMethod.objects.create(
            customer_email='mask@example.com',
            provider='square',
            payment_type='card',
            last_four_digits='1234'
        )
        
        masked = payment_method.get_masked_number()
        self.assertEqual(masked, '****-****-****-1234')
        
    def test_expired_payment_method_detection(self):
        """Test detection of expired payment methods."""
        # Create expired payment method
        expired_method = PaymentMethod.objects.create(
            customer_email='expired@example.com',
            provider='stripe',
            payment_type='card',
            last_four_digits='9999',
            expiry_month=1,
            expiry_year=2020  # Expired
        )
        
        self.assertTrue(expired_method.is_expired())
        
        # Create valid payment method
        valid_method = PaymentMethod.objects.create(
            customer_email='valid@example.com',
            provider='stripe',
            payment_type='card',
            last_four_digits='1111',
            expiry_month=12,
            expiry_year=2030  # Future
        )
        
        self.assertFalse(valid_method.is_expired())


class LineItemModelTest(TestCase):
    """Test cases for LineItem model."""
    
    def setUp(self):
        """Set up test data."""
        self.contact = Contact.objects.create(
            first_name='Test',
            last_name='Customer',
            email='customer@example.com'
        )
        
        self.invoice = Invoice.objects.create(
            customer=self.contact,
            invoice_number='LINE-TEST-001',
            total_amount=Decimal('0.00')
        )
        
    def test_line_item_total_calculation(self):
        """Test line item total calculation."""
        line_item = LineItem.objects.create(
            invoice=self.invoice,
            description='Test service',
            quantity=3,
            unit_price=Decimal('100.00'),
            tax_rate=Decimal('0.08')  # 8% tax
        )
        
        expected_subtotal = Decimal('300.00')  # 3 * 100
        expected_tax = expected_subtotal * Decimal('0.08')  # 24.00
        expected_total = expected_subtotal + expected_tax  # 324.00
        
        self.assertEqual(line_item.subtotal, expected_subtotal)
        self.assertEqual(line_item.tax_amount, expected_tax)
        self.assertEqual(line_item.total, expected_total)
