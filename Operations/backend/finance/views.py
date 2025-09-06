from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from common.permissions import IsOwnerOrReadOnly, HasRolePermission
from .models import Transaction, Invoice, InvoiceLineItem, PaymentMethod
from .serializers import (
    TransactionSerializer, CreateTransactionSerializer, ProcessPaymentSerializer,
    RefundSerializer, InvoiceSerializer, CreateInvoiceSerializer,
    PaymentMethodSerializer, CreatePaymentMethodSerializer
)
from .services.finance_service import TransactionService, InvoiceService, PaymentMethodService
import logging

logger = logging.getLogger(__name__)


class TransactionViewSet(viewsets.ModelViewSet):
    """ViewSet for Transaction operations."""
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated, HasRolePermission]
    
    def get_queryset(self):
        """Filter transactions based on query parameters."""
        queryset = super().get_queryset()
        
        # Filter by payment status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(payment_status=status_filter)
        
        # Filter by transaction type
        transaction_type = self.request.query_params.get('type')
        if transaction_type:
            queryset = queryset.filter(transaction_type=transaction_type)
        
        # Filter by customer email
        email = self.request.query_params.get('email')
        if email:
            queryset = queryset.filter(email__icontains=email)
        
        # Filter by related entities
        quote_id = self.request.query_params.get('quote_id')
        if quote_id:
            queryset = queryset.filter(related_quote_id=quote_id)
        
        trip_id = self.request.query_params.get('trip_id')
        if trip_id:
            queryset = queryset.filter(related_trip_id=trip_id)
        
        return queryset.order_by('-payment_date')
    
    def create(self, request, *args, **kwargs):
        """Create a new transaction."""
        serializer = CreateTransactionSerializer(data=request.data)
        if serializer.is_valid():
            try:
                transaction = TransactionService.create_transaction(
                    amount=serializer.validated_data['amount'],
                    currency=serializer.validated_data.get('currency', 'USD'),
                    payment_method=serializer.validated_data['payment_method'],
                    email=serializer.validated_data['email'],
                    customer_name=serializer.validated_data.get('customer_name'),
                    transaction_type=serializer.validated_data.get('transaction_type', 'payment'),
                    description=serializer.validated_data.get('description'),
                    related_quote_id=serializer.validated_data.get('related_quote_id'),
                    related_trip_id=serializer.validated_data.get('related_trip_id'),
                    billing_address=serializer.validated_data.get('billing_address')
                )
                
                response_serializer = TransactionSerializer(transaction)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
                
            except Exception as e:
                logger.error(f"Transaction creation failed: {str(e)}")
                return Response(
                    {'error': 'Transaction creation failed'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def process(self, request, pk=None):
        """Process a payment transaction."""
        transaction = self.get_object()
        serializer = ProcessPaymentSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                updated_transaction = TransactionService.process_payment(
                    transaction_id=transaction.id,
                    processor_transaction_id=serializer.validated_data['processor_transaction_id'],
                    processor_name=serializer.validated_data['processor_name'],
                    processor_fee=serializer.validated_data.get('processor_fee')
                )
                
                if updated_transaction:
                    response_serializer = TransactionSerializer(updated_transaction)
                    return Response(response_serializer.data)
                else:
                    return Response(
                        {'error': 'Transaction cannot be processed'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                    
            except Exception as e:
                logger.error(f"Payment processing failed: {str(e)}")
                return Response(
                    {'error': 'Payment processing failed'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark payment as completed."""
        transaction = self.get_object()
        
        try:
            updated_transaction = TransactionService.complete_payment(transaction.id)
            if updated_transaction:
                response_serializer = TransactionSerializer(updated_transaction)
                return Response(response_serializer.data)
            else:
                return Response(
                    {'error': 'Transaction not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
                
        except Exception as e:
            logger.error(f"Payment completion failed: {str(e)}")
            return Response(
                {'error': 'Payment completion failed'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'])
    def fail(self, request, pk=None):
        """Mark payment as failed."""
        transaction = self.get_object()
        reason = request.data.get('reason')
        
        try:
            updated_transaction = TransactionService.fail_payment(transaction.id, reason)
            if updated_transaction:
                response_serializer = TransactionSerializer(updated_transaction)
                return Response(response_serializer.data)
            else:
                return Response(
                    {'error': 'Transaction not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
                
        except Exception as e:
            logger.error(f"Payment failure update failed: {str(e)}")
            return Response(
                {'error': 'Payment failure update failed'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'])
    def refund(self, request, pk=None):
        """Create a refund for this transaction."""
        transaction = self.get_object()
        serializer = RefundSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                refund_transaction = TransactionService.create_refund(
                    original_transaction_id=transaction.id,
                    refund_amount=serializer.validated_data.get('refund_amount'),
                    reason=serializer.validated_data.get('reason')
                )
                
                if refund_transaction:
                    response_serializer = TransactionSerializer(refund_transaction)
                    return Response(response_serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(
                        {'error': 'Transaction cannot be refunded'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                    
            except Exception as e:
                logger.error(f"Refund creation failed: {str(e)}")
                return Response(
                    {'error': 'Refund creation failed'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InvoiceViewSet(viewsets.ModelViewSet):
    """ViewSet for Invoice operations."""
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated, HasRolePermission]
    
    def get_queryset(self):
        """Filter invoices based on query parameters."""
        queryset = super().get_queryset()
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by customer email
        email = self.request.query_params.get('email')
        if email:
            queryset = queryset.filter(customer_email__icontains=email)
        
        # Filter by related entities
        quote_id = self.request.query_params.get('quote_id')
        if quote_id:
            queryset = queryset.filter(related_quote_id=quote_id)
        
        trip_id = self.request.query_params.get('trip_id')
        if trip_id:
            queryset = queryset.filter(related_trip_id=trip_id)
        
        # Filter overdue invoices
        overdue = self.request.query_params.get('overdue')
        if overdue and overdue.lower() == 'true':
            from django.utils import timezone
            queryset = queryset.filter(
                due_date__lt=timezone.now().date(),
                status__in=['sent', 'viewed']
            )
        
        return queryset.order_by('-issue_date')
    
    def create(self, request, *args, **kwargs):
        """Create a new invoice."""
        serializer = CreateInvoiceSerializer(data=request.data)
        if serializer.is_valid():
            try:
                invoice = InvoiceService.create_invoice(
                    customer_email=serializer.validated_data['customer_email'],
                    customer_name=serializer.validated_data['customer_name'],
                    line_items=serializer.validated_data['line_items'],
                    due_days=serializer.validated_data.get('due_days', 30),
                    related_quote_id=serializer.validated_data.get('related_quote_id'),
                    related_trip_id=serializer.validated_data.get('related_trip_id'),
                    billing_address=serializer.validated_data.get('billing_address'),
                    description=serializer.validated_data.get('description'),
                    tax_rate=serializer.validated_data.get('tax_rate')
                )
                
                response_serializer = InvoiceSerializer(invoice)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
                
            except Exception as e:
                logger.error(f"Invoice creation failed: {str(e)}")
                return Response(
                    {'error': 'Invoice creation failed'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def send(self, request, pk=None):
        """Send invoice to customer."""
        invoice = self.get_object()
        
        try:
            updated_invoice = InvoiceService.send_invoice(invoice.id)
            if updated_invoice:
                response_serializer = InvoiceSerializer(updated_invoice)
                return Response(response_serializer.data)
            else:
                return Response(
                    {'error': 'Invoice not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
                
        except Exception as e:
            logger.error(f"Invoice sending failed: {str(e)}")
            return Response(
                {'error': 'Invoice sending failed'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'])
    def record_payment(self, request, pk=None):
        """Record a payment against this invoice."""
        invoice = self.get_object()
        transaction_id = request.data.get('transaction_id')
        
        if not transaction_id:
            return Response(
                {'error': 'Transaction ID is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            updated_invoice = InvoiceService.record_payment(invoice.id, transaction_id)
            if updated_invoice:
                response_serializer = InvoiceSerializer(updated_invoice)
                return Response(response_serializer.data)
            else:
                return Response(
                    {'error': 'Payment recording failed'},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
        except Exception as e:
            logger.error(f"Payment recording failed: {str(e)}")
            return Response(
                {'error': 'Payment recording failed'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel an invoice."""
        invoice = self.get_object()
        reason = request.data.get('reason')
        
        try:
            updated_invoice = InvoiceService.cancel_invoice(invoice.id, reason)
            if updated_invoice:
                response_serializer = InvoiceSerializer(updated_invoice)
                return Response(response_serializer.data)
            else:
                return Response(
                    {'error': 'Invoice cannot be cancelled'},
                    status=status.HTTP_400_BAD_REQUEST
                )
                
        except Exception as e:
            logger.error(f"Invoice cancellation failed: {str(e)}")
            return Response(
                {'error': 'Invoice cancellation failed'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def overdue(self, request):
        """Get all overdue invoices."""
        try:
            overdue_invoices = InvoiceService.get_overdue_invoices()
            serializer = InvoiceSerializer(overdue_invoices, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Getting overdue invoices failed: {str(e)}")
            return Response(
                {'error': 'Failed to retrieve overdue invoices'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PaymentMethodViewSet(viewsets.ModelViewSet):
    """ViewSet for PaymentMethod operations."""
    queryset = PaymentMethod.objects.filter(is_active=True)
    serializer_class = PaymentMethodSerializer
    permission_classes = [permissions.IsAuthenticated, HasRolePermission]
    
    def get_queryset(self):
        """Filter payment methods based on query parameters."""
        queryset = super().get_queryset()
        
        # Filter by customer email
        email = self.request.query_params.get('email')
        if email:
            queryset = queryset.filter(customer_email__icontains=email)
        
        # Filter by payment type
        payment_type = self.request.query_params.get('type')
        if payment_type:
            queryset = queryset.filter(payment_type=payment_type)
        
        # Show only active payment methods by default
        include_inactive = self.request.query_params.get('include_inactive')
        if not include_inactive or include_inactive.lower() != 'true':
            queryset = queryset.filter(is_active=True)
        
        return queryset.order_by('-is_default', '-created_on')
    
    def create(self, request, *args, **kwargs):
        """Create a new payment method."""
        serializer = CreatePaymentMethodSerializer(data=request.data)
        if serializer.is_valid():
            try:
                payment_method = PaymentMethodService.create_payment_method(
                    customer_email=serializer.validated_data['customer_email'],
                    payment_type=serializer.validated_data['payment_type'],
                    processor_payment_method_id=serializer.validated_data['processor_payment_method_id'],
                    processor_name=serializer.validated_data['processor_name'],
                    customer_name=serializer.validated_data.get('customer_name'),
                    last_four_digits=serializer.validated_data.get('last_four_digits'),
                    brand=serializer.validated_data.get('brand'),
                    expiry_month=serializer.validated_data.get('expiry_month'),
                    expiry_year=serializer.validated_data.get('expiry_year'),
                    is_default=serializer.validated_data.get('is_default', False)
                )
                
                response_serializer = PaymentMethodSerializer(payment_method)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
                
            except Exception as e:
                logger.error(f"Payment method creation failed: {str(e)}")
                return Response(
                    {'error': 'Payment method creation failed'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def set_default(self, request, pk=None):
        """Set this payment method as default."""
        payment_method = self.get_object()
        
        try:
            updated_payment_method = PaymentMethodService.set_default_payment_method(payment_method.id)
            if updated_payment_method:
                response_serializer = PaymentMethodSerializer(updated_payment_method)
                return Response(response_serializer.data)
            else:
                return Response(
                    {'error': 'Payment method not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
                
        except Exception as e:
            logger.error(f"Setting default payment method failed: {str(e)}")
            return Response(
                {'error': 'Setting default payment method failed'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """Deactivate this payment method."""
        payment_method = self.get_object()
        
        try:
            updated_payment_method = PaymentMethodService.deactivate_payment_method(payment_method.id)
            if updated_payment_method:
                response_serializer = PaymentMethodSerializer(updated_payment_method)
                return Response(response_serializer.data)
            else:
                return Response(
                    {'error': 'Payment method not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
                
        except Exception as e:
            logger.error(f"Payment method deactivation failed: {str(e)}")
            return Response(
                {'error': 'Payment method deactivation failed'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def by_customer(self, request):
        """Get payment methods for a specific customer."""
        customer_email = request.query_params.get('email')
        if not customer_email:
            return Response(
                {'error': 'Customer email parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            payment_methods = PaymentMethodService.get_customer_payment_methods(customer_email)
            serializer = PaymentMethodSerializer(payment_methods, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Getting customer payment methods failed: {str(e)}")
            return Response(
                {'error': 'Failed to retrieve payment methods'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
