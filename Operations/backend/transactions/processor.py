import json
import os
import requests
from django.conf import settings


def process_card_transaction(amount, card_number, expiration_date, card_code, ref_id=None, bill_to=None, ship_to=None, customer_ip='127.0.0.1'):
    """
    Process a credit card transaction through Authorize.Net
    
    Args:
        amount (str): Transaction amount
        card_number (str): Credit card number
        expiration_date (str): Card expiration date (MMYY format)
        card_code (str): CVV/CVC code
        ref_id (str, optional): Reference ID for the transaction
        bill_to (dict, optional): Billing address information
        ship_to (dict, optional): Shipping address information
        customer_ip (str, optional): Customer IP address
    
    Returns:
        dict: Response from Authorize.Net with added authorize_net_response_code
    """
    # Get Authorize.Net API credentials from Django settings
    api_login_id = settings.AUTHORIZE_NET_LOGIN_ID
    transaction_key = settings.AUTHORIZE_NET_TRANSACTION_KEY
    
    if not api_login_id or not transaction_key:
        return {
            'error': 'Authorize.Net credentials not configured',
            'details': 'Missing AUTHORIZE_NET_LOGIN_ID or AUTHORIZE_NET_TRANSACTION_KEY environment variables',
            'authorize_net_response_code': 'CONFIG_ERROR'
        }
    
    # Prepare the Authorize.Net API request
    auth_net_data = {
        "createTransactionRequest": {
            "merchantAuthentication": {
                "name": api_login_id,
                "transactionKey": transaction_key
            },
            "refId": ref_id.replace('quote_', '').replace('-', '')[:8].upper() if ref_id and 'quote_' in ref_id else (ref_id[:8] if ref_id else '12345678'),
            "transactionRequest": {
                "transactionType": "authCaptureTransaction",
                "amount": amount,
                "payment": {
                    "creditCard": {
                        "cardNumber": card_number,
                        "expirationDate": expiration_date,
                        "cardCode": card_code
                    }
                },
                "billTo": {k: v for k, v in (bill_to or {}).items() if k in ['firstName', 'lastName', 'company', 'address', 'city', 'state', 'zip', 'country']},
                "shipTo": ship_to or {},
                "customerIP": customer_ip
            }
        }
    }
    
    try:
        # Make request to Authorize.Net API
        # Use sandbox URL for testing, production URL for live transactions
        api_url = "https://apitest.authorize.net/xml/v1/request.api"  # Sandbox
        # api_url = "https://api.authorize.net/xml/v1/request.api"  # Production
        
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        response = requests.post(api_url, json=auth_net_data, headers=headers, timeout=30)
        
        # Parse Authorize.Net response - handle UTF-8 BOM
        response_text = response.text
        if response_text.startswith('\ufeff'):
            response_text = response_text[1:]  # Remove BOM
        
        auth_net_response = json.loads(response_text)
        
        # Add Authorize.Net response code to the response
        response_data = auth_net_response
        if 'transactionResponse' in auth_net_response:
            response_data['authorize_net_response_code'] = auth_net_response['transactionResponse'].get('responseCode')
        else:
            response_data['authorize_net_response_code'] = 'ERROR'
        
        return response_data
        
    except requests.exceptions.RequestException as e:
        return {
            'error': 'Failed to communicate with Authorize.Net',
            'details': str(e),
            'authorize_net_response_code': 'NETWORK_ERROR'
        }
    
    except Exception as e:
        return {
            'error': 'Transaction processing failed',
            'details': str(e),
            'authorize_net_response_code': 'PROCESSING_ERROR'
        }


def process_ach_transaction(amount, account_type, routing_number, account_number, name_on_account, 
                           echeck_type='WEB', bank_name='', ref_id=None, bill_to=None, ship_to=None, customer_ip='127.0.0.1'):
    """
    Process an ACH/eCheck transaction through Authorize.Net
    
    Args:
        amount (str): Transaction amount
        account_type (str): 'checking' or 'savings'
        routing_number (str): Bank routing number
        account_number (str): Bank account number
        name_on_account (str): Name on the bank account
        echeck_type (str, optional): Type of eCheck (WEB, PPD, CCD, etc.)
        bank_name (str, optional): Name of the bank
        ref_id (str, optional): Reference ID for the transaction
        bill_to (dict, optional): Billing address information
        ship_to (dict, optional): Shipping address information
        customer_ip (str, optional): Customer IP address
    
    Returns:
        dict: Response from Authorize.Net with added authorize_net_response_code
    """
    # Get Authorize.Net API credentials from Django settings
    api_login_id = settings.AUTHORIZE_NET_LOGIN_ID
    transaction_key = settings.AUTHORIZE_NET_TRANSACTION_KEY
    
    if not api_login_id or not transaction_key:
        return {
            'error': 'Authorize.Net credentials not configured',
            'details': 'Missing AUTHORIZE_NET_LOGIN_ID or AUTHORIZE_NET_TRANSACTION_KEY environment variables',
            'authorize_net_response_code': 'CONFIG_ERROR'
        }
    
    # Prepare the Authorize.Net API request for ACH/eCheck
    auth_net_data = {
        "createTransactionRequest": {
            "merchantAuthentication": {
                "name": api_login_id,
                "transactionKey": transaction_key
            },
            "refId": ref_id.replace('quote_', '').replace('-', '')[:8].upper() if ref_id and 'quote_' in ref_id else (ref_id[:8] if ref_id else '12345678'),
            "transactionRequest": {
                "transactionType": "authCaptureTransaction",
                "amount": amount,
                "payment": {
                    "bankAccount": {
                        "accountType": account_type,
                        "routingNumber": routing_number,
                        "accountNumber": account_number,
                        "nameOnAccount": name_on_account,
                        "echeckType": echeck_type,
                        "bankName": bank_name
                    }
                },
                "billTo": {k: v for k, v in (bill_to or {}).items() if k in ['firstName', 'lastName', 'company', 'address', 'city', 'state', 'zip', 'country']},
                "shipTo": ship_to or {},
                "customerIP": customer_ip
            }
        }
    }
    
    try:
        # Make request to Authorize.Net API
        # Use sandbox URL for testing, production URL for live transactions
        api_url = "https://apitest.authorize.net/xml/v1/request.api"  # Sandbox
        # api_url = "https://api.authorize.net/xml/v1/request.api"  # Production
        
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        response = requests.post(api_url, json=auth_net_data, headers=headers, timeout=30)
        
        # Parse Authorize.Net response - handle UTF-8 BOM
        response_text = response.text
        if response_text.startswith('\ufeff'):
            response_text = response_text[1:]  # Remove BOM
        
        auth_net_response = json.loads(response_text)
        
        # Add Authorize.Net response code to the response
        response_data = auth_net_response
        if 'transactionResponse' in auth_net_response:
            response_data['authorize_net_response_code'] = auth_net_response['transactionResponse'].get('responseCode')
        else:
            response_data['authorize_net_response_code'] = 'ERROR'
        
        return response_data
        
    except requests.exceptions.RequestException as e:
        return {
            'error': 'Failed to communicate with Authorize.Net',
            'details': str(e),
            'authorize_net_response_code': 'NETWORK_ERROR'
        }
    
    except Exception as e:
        return {
            'error': 'Transaction processing failed',
            'details': str(e),
            'authorize_net_response_code': 'PROCESSING_ERROR'
        }


if __name__ == '__main__':
    """
    Test script for transaction processing functions
    
    To run this test:
    1. Set environment variables:
       export AUTHORIZE_NET_LOGIN_ID="your_login_id"
       export AUTHORIZE_NET_TRANSACTION_KEY="your_transaction_key"
    
    2. Run: python transactions/processor.py
    """
    # Load environment variables from .env file if available
    try:
        from dotenv import load_dotenv
        load_dotenv("/home/ropolly/projects/work/JET-MAIN/.env")
    except ImportError:
        print("python-dotenv not installed, using system environment variables")
    
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
        print("  Continuing with test (will show CONFIG_ERROR)...")
    
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
    print("\nTo use in Django:")
    print("from transactions.processor import process_card_transaction, process_ach_transaction")
