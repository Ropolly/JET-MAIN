import ApiService from './ApiService';

// Interface for Authorize.Net response
export interface AuthorizeNetResponse {
  transactionResponse: {
    responseCode: string;
    authCode?: string;
    avsResultCode?: string;
    cvvResultCode?: string;
    transId?: string;
    accountNumber?: string;
    accountType?: string;
    messages: Array<{
      code: string;
      description: string;
    }>;
  };
  messages: {
    resultCode: string;
    message: Array<{
      code: string;
      text: string;
    }>;
  };
  // Custom fields added by our backend
  transaction_created?: boolean;
  transaction_id?: string;
  quote_updated?: boolean;
  new_payment_status?: string;
  remaining_balance?: string;
}

// Interface for billing address
export interface BillingAddress {
  firstName: string;
  lastName: string;
  address: string;
  city: string;
  state: string;
  zip: string;
  country?: string;
  email?: string;
  phone?: string;
}

// Interface for credit card payment data
export interface CardPaymentData {
  amount: string;
  cardNumber: string;
  expirationDate: string; // MMYY format
  cardCode: string;
  quote_id: string;
  refId?: string;
  billTo: BillingAddress;
  shipTo?: BillingAddress;
}

// Interface for ACH payment data
export interface ACHPaymentData {
  amount: string;
  accountType: 'checking' | 'savings';
  routingNumber: string;
  accountNumber: string;
  nameOnAccount: string;
  quote_id: string;
  echeckType?: string;
  bankName?: string;
  refId?: string;
  billTo: BillingAddress;
  shipTo?: BillingAddress;
}

/**
 * Service class for payment processing via Authorize.Net
 */
class PaymentService {
  
  /**
   * Process credit card payment
   */
  static async processCardPayment(paymentData: CardPaymentData): Promise<AuthorizeNetResponse> {
    try {
      const response = await ApiService.post('transactions/send/card/', paymentData);
      return response.data;
    } catch (error: any) {
      // Handle network errors or API errors
      throw new Error(error.response?.data?.error || 'Payment processing failed');
    }
  }

  /**
   * Process ACH payment
   */
  static async processACHPayment(paymentData: ACHPaymentData): Promise<AuthorizeNetResponse> {
    try {
      const response = await ApiService.post('transactions/send/ach/', paymentData);
      return response.data;
    } catch (error: any) {
      // Handle network errors or API errors
      throw new Error(error.response?.data?.error || 'Payment processing failed');
    }
  }

  /**
   * Parse Authorize.Net response and determine success/failure
   */
  static parsePaymentResponse(response: AuthorizeNetResponse) {
    const transactionResponse = response.transactionResponse;
    const messages = transactionResponse?.messages || [];
    const message = messages[0] || {};

    return {
      success: message.code === '1',
      code: message.code,
      message: message.description,
      transactionId: transactionResponse?.transId,
      authCode: transactionResponse?.authCode,
      accountNumber: transactionResponse?.accountNumber,
      accountType: transactionResponse?.accountType,
      // Our custom fields
      transactionCreated: response.transaction_created || false,
      transactionDbId: response.transaction_id,
      quoteUpdated: response.quote_updated || false,
      newPaymentStatus: response.new_payment_status,
      remainingBalance: response.remaining_balance
    };
  }

  /**
   * Get payment status badge class based on payment status
   */
  static getPaymentStatusClass(status: string): string {
    const statusClasses: Record<string, string> = {
      'pending': 'badge badge-light-warning',
      'partial': 'badge badge-light-info', 
      'paid': 'badge badge-light-success'
    };
    return statusClasses[status] || 'badge badge-light-secondary';
  }

  /**
   * Format amount for display
   */
  static formatAmount(amount: string | number): string {
    const numAmount = typeof amount === 'string' ? parseFloat(amount) : amount;
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    }).format(numAmount);
  }

  /**
   * Validate credit card number using Luhn algorithm
   */
  static validateCardNumber(cardNumber: string): boolean {
    // Remove spaces and non-digits
    const cleaned = cardNumber.replace(/\D/g, '');
    
    // Must be 13-19 digits
    if (cleaned.length < 13 || cleaned.length > 19) {
      return false;
    }

    // Luhn algorithm
    let sum = 0;
    let isEven = false;
    
    for (let i = cleaned.length - 1; i >= 0; i--) {
      let digit = parseInt(cleaned[i]);
      
      if (isEven) {
        digit *= 2;
        if (digit > 9) {
          digit -= 9;
        }
      }
      
      sum += digit;
      isEven = !isEven;
    }
    
    return sum % 10 === 0;
  }

  /**
   * Format credit card number with spaces
   */
  static formatCardNumber(cardNumber: string): string {
    const cleaned = cardNumber.replace(/\D/g, '');
    const formatted = cleaned.replace(/(\d{4})(?=\d)/g, '$1 ');
    return formatted;
  }

  /**
   * Validate routing number using checksum algorithm
   */
  static validateRoutingNumber(routingNumber: string): boolean {
    const cleaned = routingNumber.replace(/\D/g, '');
    
    // Must be exactly 9 digits
    if (cleaned.length !== 9) {
      return false;
    }

    // Routing number checksum algorithm
    const digits = cleaned.split('').map(d => parseInt(d));
    const checksum = (
      3 * (digits[0] + digits[3] + digits[6]) +
      7 * (digits[1] + digits[4] + digits[7]) +
      1 * (digits[2] + digits[5] + digits[8])
    ) % 10;
    
    return checksum === 0;
  }

  /**
   * Get test credit card numbers for sandbox testing
   */
  static getTestCards() {
    return {
      visa: '4111111111111111',
      mastercard: '5555555555554444',
      amex: '378282246310005',
      discover: '6011111111111117'
    };
  }
}

export default PaymentService;