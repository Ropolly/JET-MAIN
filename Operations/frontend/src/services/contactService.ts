/**
 * Unified Contact Service
 * 
 * Provides consistent methods for creating contacts with related records
 * (patients, staff, passengers, customers) using the unified backend API.
 */

import ApiService from '@/core/services/ApiService';

export interface ContactData {
  // Personal Information
  first_name?: string;
  last_name?: string;
  business_name?: string;
  
  // Contact Information
  email?: string;
  phone?: string;
  
  // Address Information
  address_line1?: string;
  address_line2?: string;
  city?: string;
  state?: string;
  zip?: string;
  country?: string;
  
  // Personal Details (now stored on Contact table)
  nationality?: string;
  date_of_birth?: string;  // YYYY-MM-DD format
  passport_number?: string;
  passport_expiration_date?: string;  // YYYY-MM-DD format
}

export interface PatientData {
  special_instructions?: string;
  bed_at_origin?: boolean;
  bed_at_destination?: boolean;
  status?: string;
}

export interface StaffData {
  active?: boolean;
  notes?: string;
}

export interface PassengerData {
  contact_number?: string;
  notes?: string;
  status?: string;
}

export interface ContactCreationRequest {
  // Contact data
  first_name?: string;
  last_name?: string;
  business_name?: string;
  email?: string;
  phone?: string;
  address_line1?: string;
  address_line2?: string;
  city?: string;
  state?: string;
  zip?: string;
  country?: string;
  nationality?: string;
  date_of_birth?: string;
  passport_number?: string;
  passport_expiration_date?: string;
  
  // Relationship type
  related_type: 'patient' | 'staff' | 'passenger' | 'customer';
  
  // Additional data specific to the related record
  related_data?: PatientData | StaffData | PassengerData | Record<string, any>;
}

export interface ContactCreationResponse {
  contact: any;
  related_type: string;
  patient?: any;
  staff?: any;
  passenger?: any;
  customer?: any;
  success: boolean;
  message: string;
}

export class ContactService {
  
  /**
   * Create a contact with related record (Patient, Staff, Passenger, Customer)
   */
  static async createContactWithRelated(data: ContactCreationRequest): Promise<ContactCreationResponse> {
    try {
      const response = await ApiService.post('/contacts/create-with-related/', data);
      return response.data;
    } catch (error: any) {
      throw new Error(error.response?.data?.error || error.message || 'Failed to create contact');
    }
  }
  
  /**
   * Create a patient contact
   */
  static async createPatientContact(
    contactData: ContactData,
    patientData: PatientData = {}
  ): Promise<ContactCreationResponse> {
    return this.createContactWithRelated({
      ...contactData,
      related_type: 'patient',
      related_data: patientData
    });
  }
  
  /**
   * Create a staff contact
   */
  static async createStaffContact(
    contactData: ContactData,
    staffData: StaffData = {}
  ): Promise<ContactCreationResponse> {
    return this.createContactWithRelated({
      ...contactData,
      related_type: 'staff',
      related_data: staffData
    });
  }
  
  /**
   * Create a passenger contact
   */
  static async createPassengerContact(
    contactData: ContactData,
    passengerData: PassengerData = {}
  ): Promise<ContactCreationResponse> {
    return this.createContactWithRelated({
      ...contactData,
      related_type: 'passenger',
      related_data: passengerData
    });
  }
  
  /**
   * Create a customer contact (quote contact)
   */
  static async createCustomerContact(
    contactData: ContactData
  ): Promise<ContactCreationResponse> {
    return this.createContactWithRelated({
      ...contactData,
      related_type: 'customer',
      related_data: {}
    });
  }
  
  /**
   * Validate contact data before submission
   */
  static validateContactData(data: ContactData): string[] {
    const errors: string[] = [];
    
    // Check that either personal name or business name is provided
    const hasPersonalName = (data.first_name?.trim() || data.last_name?.trim());
    const hasBusinessName = data.business_name?.trim();
    
    if (!hasPersonalName && !hasBusinessName) {
      errors.push('Either first/last name or business name is required');
    }
    
    // Validate email format if provided
    if (data.email && data.email.trim() && !data.email.includes('@')) {
      errors.push('Invalid email format');
    }
    
    // Validate date formats if provided
    if (data.date_of_birth && !this.isValidDateFormat(data.date_of_birth)) {
      errors.push('Date of birth must be in YYYY-MM-DD format');
    }
    
    if (data.passport_expiration_date && !this.isValidDateFormat(data.passport_expiration_date)) {
      errors.push('Passport expiration date must be in YYYY-MM-DD format');
    }
    
    // Validate passport expiration is after birth date if both provided
    if (data.date_of_birth && data.passport_expiration_date) {
      const birthDate = new Date(data.date_of_birth);
      const expirationDate = new Date(data.passport_expiration_date);
      
      if (expirationDate <= birthDate) {
        errors.push('Passport expiration date must be after date of birth');
      }
    }
    
    return errors;
  }
  
  /**
   * Check if a string is in valid YYYY-MM-DD format
   */
  private static isValidDateFormat(dateString: string): boolean {
    const dateRegex = /^\d{4}-\d{2}-\d{2}$/;
    if (!dateRegex.test(dateString)) {
      return false;
    }
    
    const date = new Date(dateString);
    return date instanceof Date && !isNaN(date.getTime());
  }
  
  /**
   * Format form data for API submission
   */
  static formatContactDataForAPI(formData: Record<string, any>): ContactData {
    return {
      first_name: formData.firstName?.trim() || formData.first_name?.trim() || '',
      last_name: formData.lastName?.trim() || formData.last_name?.trim() || '',
      business_name: formData.businessName?.trim() || formData.business_name?.trim() || '',
      email: formData.email?.trim() || '',
      phone: formData.phone?.trim() || '',
      address_line1: formData.addressLine1?.trim() || formData.address_line1?.trim() || '',
      address_line2: formData.addressLine2?.trim() || formData.address_line2?.trim() || '',
      city: formData.city?.trim() || '',
      state: formData.state?.trim() || '',
      zip: formData.zip?.trim() || '',
      country: formData.country?.trim() || '',
      nationality: formData.nationality?.trim() || '',
      date_of_birth: formData.dateOfBirth || formData.date_of_birth || '',
      passport_number: formData.passportNumber?.trim() || formData.passport_number?.trim() || '',
      passport_expiration_date: formData.passportExpirationDate || formData.passport_expiration_date || ''
    };
  }
  
  /**
   * Get display name for a contact
   */
  static getContactDisplayName(contact: any): string {
    if (!contact) return 'Unknown Contact';
    
    if (contact.business_name?.trim()) {
      return contact.business_name.trim();
    }
    
    const firstName = contact.first_name?.trim() || '';
    const lastName = contact.last_name?.trim() || '';
    const fullName = `${firstName} ${lastName}`.trim();
    
    return fullName || contact.email || 'Unnamed Contact';
  }
  
  /**
   * Get contact type display name
   */
  static getContactTypeDisplayName(contactType: string): string {
    const types: Record<string, string> = {
      'patient': 'Patient',
      'staff': 'Staff Member',
      'passenger': 'Passenger',
      'customer': 'Customer',
      'general': 'General Contact'
    };
    
    return types[contactType.toLowerCase()] || 'Contact';
  }
}

export default ContactService;