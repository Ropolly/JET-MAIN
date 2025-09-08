from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .processor import process_card_transaction, process_ach_transaction


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_card_transaction(request):
    """
    Process card transaction through Authorize.Net
    """
    transaction_data = request.data
    
    # Call the processing function
    result = process_card_transaction(
        amount=transaction_data.get('amount'),
        card_number=transaction_data.get('cardNumber'),
        expiration_date=transaction_data.get('expirationDate'),
        card_code=transaction_data.get('cardCode'),
        ref_id=transaction_data.get('refId'),
        bill_to=transaction_data.get('billTo'),
        ship_to=transaction_data.get('shipTo'),
        customer_ip=request.META.get('REMOTE_ADDR', '127.0.0.1')
    )
    
    return Response(result, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_ach_transaction(request):
    """
    Process ACH transaction through Authorize.Net
    """
    transaction_data = request.data
    
    # Call the processing function
    result = process_ach_transaction(
        amount=transaction_data.get('amount'),
        account_type=transaction_data.get('accountType', 'checking'),
        routing_number=transaction_data.get('routingNumber'),
        account_number=transaction_data.get('accountNumber'),
        name_on_account=transaction_data.get('nameOnAccount'),
        echeck_type=transaction_data.get('echeckType', 'WEB'),
        bank_name=transaction_data.get('bankName', ''),
        ref_id=transaction_data.get('refId'),
        bill_to=transaction_data.get('billTo'),
        ship_to=transaction_data.get('shipTo'),
        customer_ip=request.META.get('REMOTE_ADDR', '127.0.0.1')
    )
    
    return Response(result, status=status.HTTP_200_OK)


if __name__ == '__main__':
    """
    Test script for transaction processing functions
    
    To run this test:
    1. Set environment variables:
       export AUTHORIZE_NET_LOGIN_ID="your_login_id"
       export AUTHORIZE_NET_TRANSACTION_KEY="your_transaction_key"
    
    2. Run: python transactions/views.py
    """
    DOT_ENV_PATH = "/home/ropolly/projects/work/JET-MAIN/.env"
    from dotenv import load_dotenv
    load_dotenv()
    
    print("Testing Transaction Processing Functions")
    print("=" * 50)
    
    # Check if environment variables are set
    login_id = os.getenv('AUTHORIZE_NET_LOGIN_ID')
    transaction_key = os.getenv('AUTHORIZE_NET_TRANSACTION_KEY')
    
    if login_id and transaction_key:
        print(f"✓ Environment variables configured:")
        print(f"  AUTHORIZE_NET_LOGIN_ID: {login_id[:4]}***")
        print(f"  AUTHORIZE_NET_TRANSACTION_KEY: {transaction_key[:4]}***")
    else:
        print("⚠ Environment variables not set:")
        print("  Please set AUTHORIZE_NET_LOGIN_ID and AUTHORIZE_NET_TRANSACTION_KEY")
        print("  Skipping actual API tests...")
    
    print("\n" + "=" * 50)
    print("Testing Card Transaction Function")
    print("=" * 50)
    
    # Test card transaction function
    card_result = process_card_transaction(
        amount='10.00',
        card_number='4111111111111111',  # Test card number
        expiration_date='1225',  # MMYY format
        card_code='123',
        ref_id='test_card_001',
        bill_to={
            'firstName': 'John',
            'lastName': 'Doe',
            'address': '123 Test St',
            'city': 'Test City',
            'state': 'CA',
            'zip': '12345',
            'country': 'US'
        },
        customer_ip='127.0.0.1'
    )
    
    print("Card Transaction Result:")
    print(json.dumps(card_result, indent=2))
    
    print("\n" + "=" * 50)
    print("Testing ACH Transaction Function")
    print("=" * 50)
    
    # Test ACH transaction function
    ach_result = process_ach_transaction(
        amount='25.00',
        account_type='checking',
        routing_number='121042882',  # Test routing number
        account_number='123456789',  # Test account number
        name_on_account='John Doe',
        echeck_type='WEB',
        bank_name='Test Bank',
        ref_id='test_ach_001',
        bill_to={
            'firstName': 'John',
            'lastName': 'Doe',
            'address': '123 Test St',
            'city': 'Test City',
            'state': 'CA',
            'zip': '12345',
            'country': 'US'
        },
        customer_ip='127.0.0.1'
    )
    
    print("ACH Transaction Result:")
    print(json.dumps(ach_result, indent=2))
    
    print("\n" + "=" * 50)
    print("Test Summary")
    print("=" * 50)
    print("Functions tested:")
    print("- process_card_transaction()")
    print("- process_ach_transaction()")
    print("\nEndpoints available:")
    print("- POST /transactions/send/card/")
    print("- POST /transactions/send/ach/")
    print("\nNote: Endpoints require JWT authentication")
