"""
Django test cases for payment processing functionality.

Converted from custom test scripts to proper Django TestCase.
"""

from django.test import TestCase
from unittest.mock import patch, Mock
from decimal import Decimal
from finance.models import Transaction, PaymentMethod
from finance.services.payment_processor import PaymentProcessorService
from contacts.models import Contact


class PaymentProcessorTestCase(TestCase):
    """Test case for payment processing functionality."""
    
    def setUp(self):
        """Set up test data for payment processor tests."""
        self.contact = Contact.objects.create(
            first_name="John",
            last_name="Doe",
            email="john.doe@test.com"
        )
        
        self.transaction = Transaction.objects.create(
            amount=Decimal('1500.00'),
            currency='USD',
            transaction_type='payment',
            payment_status='created',
            customer_name='John Doe',
            email='john.doe@test.com',
            description='Test flight payment'
        )
        
        self.payment_method = PaymentMethod.objects.create(
            contact=self.contact,
            method_type='credit_card',
            is_default=True,
            card_last_four='1234',
            card_brand='visa'
        )
        
        self.stripe_service = PaymentProcessorService(provider='stripe')
        self.square_service = PaymentProcessorService(provider='square')
    
    def test_stripe_provider_initialization(self):
        """Test Stripe payment processor initialization."""
        service = PaymentProcessorService(provider='stripe')
        
        self.assertEqual(service.provider, 'stripe')
        self.assertEqual(service.base_url, 'https://api.stripe.com/v1')
    
    def test_square_provider_initialization(self):
        """Test Square payment processor initialization."""
        service = PaymentProcessorService(provider='square')
        
        self.assertEqual(service.provider, 'square')
        # Should use sandbox URL by default
        self.assertIn('sandbox', service.base_url)
    
    @patch('finance.services.payment_processor.requests.post')
    def test_stripe_payment_intent_creation_success(self, mock_post):
        """Test successful Stripe payment intent creation."""
        # Mock successful Stripe response
        mock_response = Mock()
        mock_response.json.return_value = {
            'id': 'pi_test_123',
            'client_secret': 'pi_test_123_secret',
            'amount': 150000,  # $1500 in cents
            'currency': 'usd',
            'status': 'requires_payment_method'
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        # Test payment intent creation
        result = self.stripe_service.create_payment_intent(
            amount=Decimal('1500.00'),
            currency='USD',
            customer_email='test@example.com',
            description='Test payment'
        )
        
        # Assertions
        self.assertIsNotNone(result)
        self.assertEqual(result['id'], 'pi_test_123')
        self.assertEqual(result['amount'], 1500.0)
        self.assertEqual(result['currency'], 'USD')
        self.assertEqual(result['provider'], 'stripe')
        mock_post.assert_called_once()
    
    @patch('finance.services.payment_processor.requests.post')
    def test_stripe_payment_intent_creation_failure(self, mock_post):
        """Test Stripe payment intent creation failure."""
        # Mock failed response
        mock_post.side_effect = Exception("API Error")
        
        # Test payment intent creation
        result = self.stripe_service.create_payment_intent(
            amount=Decimal('1500.00'),
            currency='USD'
        )
        
        # Should return None on failure
        self.assertIsNone(result)
    
    @patch('finance.services.payment_processor.requests.post')
    def test_square_payment_creation_success(self, mock_post):
        """Test successful Square payment creation."""
        # Mock successful Square response
        mock_response = Mock()
        mock_response.json.return_value = {
            'payment': {
                'id': 'sq_test_123',
                'amount_money': {
                    'amount': 150000,  # $1500 in cents
                    'currency': 'USD'
                },
                'status': 'COMPLETED'
            }
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        # Test payment creation
        result = self.square_service.create_payment_intent(
            amount=Decimal('1500.00'),
            currency='USD',
            description='Test payment'
        )
        
        # Assertions
        self.assertIsNotNone(result)
        self.assertEqual(result['id'], 'sq_test_123')
        self.assertEqual(result['amount'], 1500.0)
        self.assertEqual(result['provider'], 'square')
    
    @patch('finance.services.payment_processor.requests.post')
    def test_stripe_payment_confirmation_success(self, mock_post):
        """Test successful Stripe payment confirmation."""
        # Mock successful confirmation response
        mock_response = Mock()
        mock_response.json.return_value = {
            'id': 'pi_test_123',
            'status': 'succeeded',
            'amount': 150000,
            'currency': 'usd'
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        # Test payment confirmation
        result = self.stripe_service.confirm_payment('pi_test_123', 'pm_test_456')
        
        # Assertions
        self.assertIsNotNone(result)
        self.assertEqual(result['status'], 'succeeded')
        self.assertEqual(result['provider'], 'stripe')
    
    @patch('finance.services.payment_processor.requests.get')
    def test_square_payment_status_check(self, mock_get):
        """Test Square payment status check."""
        # Mock successful status response
        mock_response = Mock()
        mock_response.json.return_value = {
            'payment': {
                'id': 'sq_test_123',
                'status': 'COMPLETED',
                'amount_money': {
                    'amount': 150000,
                    'currency': 'USD'
                }
            }
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Test status check
        result = self.square_service.confirm_payment('sq_test_123')
        
        # Assertions
        self.assertIsNotNone(result)
        self.assertEqual(result['status'], 'COMPLETED')
        self.assertEqual(result['provider'], 'square')
    
    @patch('finance.services.payment_processor.requests.post')
    def test_stripe_refund_creation_success(self, mock_post):
        """Test successful Stripe refund creation."""
        # Mock successful refund response
        mock_response = Mock()
        mock_response.json.return_value = {
            'id': 're_test_123',
            'amount': 150000,
            'currency': 'usd',
            'status': 'succeeded'
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        # Test refund creation
        result = self.stripe_service.create_refund(
            'pi_test_123',
            amount=Decimal('1500.00'),
            reason='requested_by_customer'
        )
        
        # Assertions
        self.assertIsNotNone(result)
        self.assertEqual(result['id'], 're_test_123')
        self.assertEqual(result['amount'], 1500.0)
        self.assertEqual(result['status'], 'succeeded')
    
    @patch('finance.services.payment_processor.requests.post')
    def test_square_refund_creation_success(self, mock_post):
        """Test successful Square refund creation."""
        # Mock successful refund response
        mock_response = Mock()
        mock_response.json.return_value = {
            'refund': {
                'id': 'sq_refund_123',
                'amount_money': {
                    'amount': 150000,
                    'currency': 'USD'
                },
                'status': 'COMPLETED'
            }
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        # Test refund creation
        result = self.square_service.create_refund(
            'sq_test_123',
            amount=Decimal('1500.00'),
            reason='Customer request'
        )
        
        # Assertions
        self.assertIsNotNone(result)
        self.assertEqual(result['id'], 'sq_refund_123')
        self.assertEqual(result['amount'], 1500.0)
        self.assertEqual(result['status'], 'COMPLETED')
    
    @patch('finance.services.payment_processor.PaymentProcessorService.create_payment_intent')
    @patch('finance.services.payment_processor.TransactionService.process_payment')
    def test_transaction_processing_success(self, mock_process_payment, mock_create_intent):
        """Test successful transaction processing."""
        # Mock payment intent creation
        mock_create_intent.return_value = {
            'id': 'pi_test_123',
            'client_secret': 'pi_test_123_secret',
            'amount': 1500.0,
            'currency': 'USD',
            'status': 'requires_payment_method'
        }
        
        # Mock transaction processing
        mock_process_payment.return_value = self.transaction
        
        # Test transaction processing
        result = self.stripe_service.process_transaction(str(self.transaction.id))
        
        # Assertions
        self.assertIsNotNone(result)
        mock_create_intent.assert_called_once()
        mock_process_payment.assert_called_once()
    
    def test_transaction_processing_invalid_transaction(self):
        """Test transaction processing with invalid transaction ID."""
        result = self.stripe_service.process_transaction('invalid-id')
        self.assertIsNone(result)
    
    def test_unsupported_provider(self):
        """Test unsupported payment provider."""
        service = PaymentProcessorService(provider='unsupported')
        
        result = service.create_payment_intent(
            amount=Decimal('100.00'),
            currency='USD'
        )
        
        self.assertIsNone(result)
    
    @patch('finance.services.payment_processor.requests.post')
    def test_network_error_handling(self, mock_post):
        """Test network error handling."""
        # Mock network error
        mock_post.side_effect = Exception("Network timeout")
        
        # Test payment intent creation with error
        result = self.stripe_service.create_payment_intent(
            amount=Decimal('100.00'),
            currency='USD'
        )
        
        self.assertIsNone(result)
    
    def test_api_key_configuration(self):
        """Test API key configuration for different providers."""
        # Test with missing API key (should handle gracefully)
        with patch('finance.services.payment_processor.getattr', return_value=None):
            service = PaymentProcessorService(provider='stripe')
            result = service.create_payment_intent(
                amount=Decimal('100.00'),
                currency='USD'
            )
            self.assertIsNone(result)
    
    def test_convenience_functions(self):
        """Test convenience functions."""
        from finance.services.payment_processor import create_payment_intent, process_transaction
        
        # Test create_payment_intent convenience function
        with patch.object(PaymentProcessorService, 'create_payment_intent') as mock_create:
            mock_create.return_value = {'id': 'test_123'}
            
            result = create_payment_intent(
                amount=Decimal('100.00'),
                currency='USD'
            )
            
            self.assertIsNotNone(result)
            mock_create.assert_called_once()
        
        # Test process_transaction convenience function
        with patch.object(PaymentProcessorService, 'process_transaction') as mock_process:
            mock_process.return_value = self.transaction
            
            result = process_transaction(str(self.transaction.id))
            
            self.assertIsNotNone(result)
            mock_process.assert_called_once()
