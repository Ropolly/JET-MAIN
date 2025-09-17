import os
import secrets
import re
from datetime import datetime, timedelta
from django.utils import timezone
from django.conf import settings
from twilio.rest import Client
from twilio.base.exceptions import TwilioException
from api.models import SMSVerificationCode
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)


class TwilioService:
    def __init__(self):
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.phone_number = os.getenv('TWILIO_PHONE_NUMBER')

        if not all([self.account_sid, self.auth_token, self.phone_number]):
            raise ValueError("Missing Twilio configuration. Please check your environment variables.")

        self.client = Client(self.account_sid, self.auth_token)

    def format_phone_number(self, phone_number):
        """
        Format phone number to E.164 format (+1XXXXXXXXXX)
        """
        # Remove all non-digit characters
        digits_only = re.sub(r'\D', '', phone_number)

        # If it's 10 digits, assume it's US number and add +1
        if len(digits_only) == 10:
            return f"+1{digits_only}"

        # If it's 11 digits and starts with 1, format as US number
        if len(digits_only) == 11 and digits_only.startswith('1'):
            return f"+{digits_only}"

        # If it already starts with +, return as is (assumed to be properly formatted)
        if phone_number.startswith('+'):
            return phone_number

        # Otherwise, assume it's a US number and add +1
        return f"+1{digits_only}"

    def validate_phone_number(self, phone_number):
        """
        Validate phone number format
        """
        formatted_number = self.format_phone_number(phone_number)

        # Basic validation for E.164 format
        e164_pattern = r'^\+[1-9]\d{1,14}$'

        if not re.match(e164_pattern, formatted_number):
            return False, "Invalid phone number format"

        return True, formatted_number

    def generate_verification_code(self):
        """
        Generate a 6-digit verification code
        """
        return f"{secrets.randbelow(900000) + 100000:06d}"

    def create_verification_code(self, phone_number, user=None):
        """
        Create a new SMS verification code record
        """
        # Validate and format phone number
        is_valid, formatted_number = self.validate_phone_number(phone_number)
        if not is_valid:
            raise ValueError(formatted_number)  # formatted_number contains error message

        # Check rate limiting - only allow one code per phone number every 30 seconds
        thirty_seconds_ago = timezone.now() - timedelta(seconds=30)
        recent_code = SMSVerificationCode.objects.filter(
            phone_number=formatted_number,
            created_at__gte=thirty_seconds_ago
        ).first()

        if recent_code:
            raise ValueError("Please wait 30 seconds before requesting another code")

        # Generate verification code
        code = self.generate_verification_code()

        # Set expiration (5 minutes from now)
        expires_at = timezone.now() + timedelta(minutes=5)

        # Create verification code record
        verification_code = SMSVerificationCode.objects.create(
            phone_number=formatted_number,
            code=code,
            user=user,
            expires_at=expires_at
        )

        return verification_code

    def send_sms_verification_code(self, phone_number, user=None):
        """
        Send SMS verification code to the provided phone number
        """
        try:
            # Create verification code
            verification_code = self.create_verification_code(phone_number, user)

            # Send SMS
            message_body = f"Your JET ICU verification code is: {verification_code.code}. This code expires in 5 minutes."

            message = self.client.messages.create(
                body=message_body,
                from_=self.phone_number,
                to=verification_code.phone_number
            )

            logger.info(f"SMS sent successfully to {verification_code.phone_number}. Message SID: {message.sid}")

            return {
                'success': True,
                'message': 'Verification code sent successfully',
                'phone_number': verification_code.phone_number,
                'expires_at': verification_code.expires_at
            }

        except ValueError as e:
            logger.error(f"Validation error: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
        except TwilioException as e:
            logger.error(f"Twilio error: {str(e)}")
            return {
                'success': False,
                'error': 'Failed to send SMS. Please check the phone number and try again.'
            }
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return {
                'success': False,
                'error': 'An unexpected error occurred. Please try again.'
            }

    def verify_sms_code(self, phone_number, code, user=None):
        """
        Verify the SMS code entered by the user
        """
        try:
            # Validate and format phone number
            is_valid, formatted_number = self.validate_phone_number(phone_number)
            if not is_valid:
                return {
                    'success': False,
                    'error': formatted_number  # contains error message
                }

            # Find the verification code
            verification_code = SMSVerificationCode.objects.filter(
                phone_number=formatted_number,
                code=code,
                verified=False
            ).order_by('-created_at').first()

            if not verification_code:
                return {
                    'success': False,
                    'error': 'Invalid verification code'
                }

            # Increment attempts
            verification_code.attempts += 1
            verification_code.save()

            # Check if too many attempts
            if not verification_code.can_attempt():
                return {
                    'success': False,
                    'error': 'Too many verification attempts. Please request a new code.'
                }

            # Check if expired
            if verification_code.is_expired():
                return {
                    'success': False,
                    'error': 'Verification code has expired. Please request a new code.'
                }

            # Mark as verified
            verification_code.verified = True
            verification_code.save()

            # If user is provided, mark their phone as verified
            if user and hasattr(user, 'profile'):
                user.profile.phone_verified = True
                user.profile.save()

            return {
                'success': True,
                'message': 'Phone number verified successfully',
                'phone_number': formatted_number
            }

        except Exception as e:
            logger.error(f"Error verifying SMS code: {str(e)}")
            return {
                'success': False,
                'error': 'An error occurred while verifying the code. Please try again.'
            }

    def cleanup_expired_codes(self):
        """
        Clean up expired verification codes (called periodically)
        """
        expired_codes = SMSVerificationCode.objects.filter(
            expires_at__lt=timezone.now(),
            verified=False
        )
        count = expired_codes.count()
        expired_codes.delete()
        logger.info(f"Cleaned up {count} expired verification codes")
        return count


# Singleton instance
twilio_service = TwilioService()