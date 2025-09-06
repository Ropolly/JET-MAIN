"""
Payment Processing Service for Finance Operations

Moved from utils/paymentprocess/ to finance/services/payment_processor.py
This service handles payment processing integration with external providers.
"""

import requests
import logging
from decimal import Decimal
from django.conf import settings
from django.utils import timezone
from ..models import Transaction, PaymentMethod
from .finance_service import TransactionService

logger = logging.getLogger(__name__)


class PaymentProcessorService:
    """
    Service for handling payment processing with external providers
    """
    
    def __init__(self, provider='stripe'):
        self.provider = provider
        self.api_key = self._get_api_key()
        self.base_url = self._get_base_url()
        
    def _get_api_key(self):
        """Get API key for the payment provider"""
        if self.provider == 'stripe':
            return getattr(settings, 'STRIPE_SECRET_KEY', None)
        elif self.provider == 'square':
            return getattr(settings, 'SQUARE_ACCESS_TOKEN', None)
        elif self.provider == 'paypal':
            return getattr(settings, 'PAYPAL_CLIENT_SECRET', None)
        return None
    
    def _get_base_url(self):
        """Get base URL for the payment provider API"""
        if self.provider == 'stripe':
            return 'https://api.stripe.com/v1'
        elif self.provider == 'square':
            sandbox = getattr(settings, 'SQUARE_SANDBOX', True)
            return 'https://connect.squareupsandbox.com/v2' if sandbox else 'https://connect.squareup.com/v2'
        elif self.provider == 'paypal':
            sandbox = getattr(settings, 'PAYPAL_SANDBOX', True)
            return 'https://api.sandbox.paypal.com' if sandbox else 'https://api.paypal.com'
        return None
    
    def create_payment_intent(self, amount, currency='USD', customer_email=None, 
                            description=None, metadata=None):
        """
        Create a payment intent with the payment provider
        
        Args:
            amount: Payment amount in cents/smallest currency unit
            currency: Currency code (default: USD)
            customer_email: Customer email address
            description: Payment description
            metadata: Additional metadata
            
        Returns:
            dict: Payment intent data or None if error
        """
        try:
            if self.provider == 'stripe':
                return self._create_stripe_payment_intent(
                    amount, currency, customer_email, description, metadata
                )
            elif self.provider == 'square':
                return self._create_square_payment(
                    amount, currency, customer_email, description, metadata
                )
            else:
                logger.error(f"Unsupported payment provider: {self.provider}")
                return None
                
        except Exception as e:
            logger.error(f"Error creating payment intent: {str(e)}")
            return None
    
    def _create_stripe_payment_intent(self, amount, currency, customer_email, description, metadata):
        """Create Stripe payment intent"""
        if not self.api_key:
            logger.error("Stripe API key not configured")
            return None
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        data = {
            'amount': int(amount * 100),  # Convert to cents
            'currency': currency.lower(),
            'automatic_payment_methods[enabled]': 'true'
        }
        
        if customer_email:
            data['receipt_email'] = customer_email
        
        if description:
            data['description'] = description
        
        if metadata:
            for key, value in metadata.items():
                data[f'metadata[{key}]'] = str(value)
        
        try:
            response = requests.post(
                f'{self.base_url}/payment_intents',
                headers=headers,
                data=data,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            logger.info(f"Created Stripe payment intent: {result['id']}")
            
            return {
                'id': result['id'],
                'client_secret': result['client_secret'],
                'amount': result['amount'] / 100,  # Convert back to dollars
                'currency': result['currency'].upper(),
                'status': result['status'],
                'provider': 'stripe'
            }
            
        except requests.RequestException as e:
            logger.error(f"Stripe API error: {str(e)}")
            return None
    
    def _create_square_payment(self, amount, currency, customer_email, description, metadata):
        """Create Square payment"""
        if not self.api_key:
            logger.error("Square access token not configured")
            return None
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'Square-Version': '2023-10-18'
        }
        
        # Square uses cents for USD
        amount_money = {
            'amount': int(amount * 100),
            'currency': currency.upper()
        }
        
        data = {
            'source_id': 'EXTERNAL',  # This would be replaced with actual payment source
            'amount_money': amount_money,
            'idempotency_key': f"payment_{timezone.now().timestamp()}"
        }
        
        if description:
            data['note'] = description
        
        try:
            response = requests.post(
                f'{self.base_url}/payments',
                headers=headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            payment = result.get('payment', {})
            
            logger.info(f"Created Square payment: {payment.get('id')}")
            
            return {
                'id': payment.get('id'),
                'amount': payment.get('amount_money', {}).get('amount', 0) / 100,
                'currency': payment.get('amount_money', {}).get('currency', currency),
                'status': payment.get('status', 'unknown'),
                'provider': 'square'
            }
            
        except requests.RequestException as e:
            logger.error(f"Square API error: {str(e)}")
            return None
    
    def confirm_payment(self, payment_intent_id, payment_method_id=None):
        """
        Confirm a payment intent
        
        Args:
            payment_intent_id: Payment intent ID from provider
            payment_method_id: Payment method ID (if required)
            
        Returns:
            dict: Payment confirmation data or None if error
        """
        try:
            if self.provider == 'stripe':
                return self._confirm_stripe_payment(payment_intent_id, payment_method_id)
            elif self.provider == 'square':
                return self._get_square_payment_status(payment_intent_id)
            else:
                logger.error(f"Unsupported payment provider: {self.provider}")
                return None
                
        except Exception as e:
            logger.error(f"Error confirming payment: {str(e)}")
            return None
    
    def _confirm_stripe_payment(self, payment_intent_id, payment_method_id):
        """Confirm Stripe payment intent"""
        if not self.api_key:
            logger.error("Stripe API key not configured")
            return None
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        data = {}
        if payment_method_id:
            data['payment_method'] = payment_method_id
        
        try:
            response = requests.post(
                f'{self.base_url}/payment_intents/{payment_intent_id}/confirm',
                headers=headers,
                data=data,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            logger.info(f"Confirmed Stripe payment: {payment_intent_id}")
            
            return {
                'id': result['id'],
                'status': result['status'],
                'amount': result['amount'] / 100,
                'currency': result['currency'].upper(),
                'provider': 'stripe'
            }
            
        except requests.RequestException as e:
            logger.error(f"Stripe confirmation error: {str(e)}")
            return None
    
    def _get_square_payment_status(self, payment_id):
        """Get Square payment status"""
        if not self.api_key:
            logger.error("Square access token not configured")
            return None
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Square-Version': '2023-10-18'
        }
        
        try:
            response = requests.get(
                f'{self.base_url}/payments/{payment_id}',
                headers=headers,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            payment = result.get('payment', {})
            
            return {
                'id': payment.get('id'),
                'status': payment.get('status', 'unknown'),
                'amount': payment.get('amount_money', {}).get('amount', 0) / 100,
                'currency': payment.get('amount_money', {}).get('currency', 'USD'),
                'provider': 'square'
            }
            
        except requests.RequestException as e:
            logger.error(f"Square status check error: {str(e)}")
            return None
    
    def create_refund(self, payment_id, amount=None, reason=None):
        """
        Create a refund for a payment
        
        Args:
            payment_id: Original payment ID
            amount: Refund amount (None for full refund)
            reason: Refund reason
            
        Returns:
            dict: Refund data or None if error
        """
        try:
            if self.provider == 'stripe':
                return self._create_stripe_refund(payment_id, amount, reason)
            elif self.provider == 'square':
                return self._create_square_refund(payment_id, amount, reason)
            else:
                logger.error(f"Unsupported payment provider: {self.provider}")
                return None
                
        except Exception as e:
            logger.error(f"Error creating refund: {str(e)}")
            return None
    
    def _create_stripe_refund(self, payment_intent_id, amount, reason):
        """Create Stripe refund"""
        if not self.api_key:
            logger.error("Stripe API key not configured")
            return None
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        data = {
            'payment_intent': payment_intent_id
        }
        
        if amount:
            data['amount'] = int(amount * 100)  # Convert to cents
        
        if reason:
            data['reason'] = reason
        
        try:
            response = requests.post(
                f'{self.base_url}/refunds',
                headers=headers,
                data=data,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            logger.info(f"Created Stripe refund: {result['id']}")
            
            return {
                'id': result['id'],
                'amount': result['amount'] / 100,
                'currency': result['currency'].upper(),
                'status': result['status'],
                'provider': 'stripe'
            }
            
        except requests.RequestException as e:
            logger.error(f"Stripe refund error: {str(e)}")
            return None
    
    def _create_square_refund(self, payment_id, amount, reason):
        """Create Square refund"""
        if not self.api_key:
            logger.error("Square access token not configured")
            return None
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
            'Square-Version': '2023-10-18'
        }
        
        data = {
            'payment_id': payment_id,
            'idempotency_key': f"refund_{timezone.now().timestamp()}"
        }
        
        if amount:
            data['amount_money'] = {
                'amount': int(amount * 100),
                'currency': 'USD'
            }
        
        if reason:
            data['reason'] = reason
        
        try:
            response = requests.post(
                f'{self.base_url}/refunds',
                headers=headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            refund = result.get('refund', {})
            
            logger.info(f"Created Square refund: {refund.get('id')}")
            
            return {
                'id': refund.get('id'),
                'amount': refund.get('amount_money', {}).get('amount', 0) / 100,
                'currency': refund.get('amount_money', {}).get('currency', 'USD'),
                'status': refund.get('status', 'unknown'),
                'provider': 'square'
            }
            
        except requests.RequestException as e:
            logger.error(f"Square refund error: {str(e)}")
            return None
    
    def process_transaction(self, transaction_id, payment_method_data=None):
        """
        Process a transaction through the payment provider
        
        Args:
            transaction_id: Internal transaction ID
            payment_method_data: Payment method information
            
        Returns:
            Transaction instance or None if error
        """
        try:
            transaction = Transaction.objects.get(id=transaction_id)
            
            if transaction.payment_status != 'created':
                logger.error(f"Transaction {transaction_id} not in processable state")
                return None
            
            # Create payment intent
            payment_intent = self.create_payment_intent(
                amount=transaction.amount,
                currency=transaction.currency,
                customer_email=transaction.email,
                description=transaction.description,
                metadata={
                    'transaction_id': str(transaction.id),
                    'customer_name': transaction.customer_name or ''
                }
            )
            
            if not payment_intent:
                logger.error(f"Failed to create payment intent for transaction {transaction_id}")
                return None
            
            # Update transaction with payment provider details
            updated_transaction = TransactionService.process_payment(
                transaction_id=transaction.id,
                processor_transaction_id=payment_intent['id'],
                processor_name=self.provider
            )
            
            return updated_transaction
            
        except Transaction.DoesNotExist:
            logger.error(f"Transaction not found: {transaction_id}")
            return None
        except Exception as e:
            logger.error(f"Error processing transaction {transaction_id}: {str(e)}")
            return None


# Convenience functions for backward compatibility
def create_payment_intent(amount, currency='USD', customer_email=None, description=None):
    """Create a payment intent"""
    service = PaymentProcessorService()
    return service.create_payment_intent(amount, currency, customer_email, description)


def process_transaction(transaction_id, payment_method_data=None):
    """Process a transaction"""
    service = PaymentProcessorService()
    return service.process_transaction(transaction_id, payment_method_data)
