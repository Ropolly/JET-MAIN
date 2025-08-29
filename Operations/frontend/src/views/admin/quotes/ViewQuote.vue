<template>
  <!-- Associated Trip Alert -->
  <div v-if="associatedTrip" class="alert alert-primary d-flex align-items-center justify-content-between mb-5">
    <div class="d-flex align-items-center">
      <KTIcon icon-name="airplane" icon-class="fs-2x text-primary me-4" />
      <div>
        <div class="fw-bold fs-6">This quote has been converted to a trip</div>
        <div class="text-gray-700 fs-7">
          Trip #{{ associatedTrip.trip_number || associatedTrip.id?.slice(0, 8) }}
          <span class="mx-2">•</span>
          {{ getPatientName() }}
          <span class="mx-2">•</span>
          {{ getRouteInfo() }}
          <span class="mx-2">•</span>
          <span class="badge badge-primary fs-8">
            {{ associatedTrip.status }}
          </span>
        </div>
      </div>
    </div>
    <button @click="viewTrip" class="btn btn-sm btn-primary">
      View Trip
      <KTIcon icon-name="arrow-right" icon-class="fs-5 ms-1" />
    </button>
  </div>

  <div class="card">     
    <!--begin::Body-->
    <div class="card-body p-lg-20">
      <!--begin::Layout-->
      <div class="d-flex flex-column flex-xl-row">
        <!--begin::Content-->
        <div class="flex-lg-row-fluid me-xl-18 mb-10 mb-xl-0">
          <!--begin::Quote content-->
          <div class="mt-n1">                                    
            <!--begin::Top-->
            <div class="d-flex flex-stack pb-10">
              <!--begin::Logo-->
              <a href="#">
                <div class="d-flex align-items-center">
                  <div class="symbol symbol-50px me-3">
                    <div class="symbol-label bg-primary">
                      <KTIcon icon-name="airplane" icon-class="fs-2x text-white" />
                    </div>
                  </div>
                  <div class="d-flex flex-column">
                    <div class="fs-3 fw-bold text-gray-800">JET ICU</div>
                    <div class="fs-7 text-muted">Medical Transport Services</div>
                  </div>
                </div>
              </a>
              <!--end::Logo-->
                                    
              <!--begin::Action-->            
              <div class="d-flex gap-3">
                <!-- Actions moved to toolbar -->
              </div>                 
              <!--end::Action--> 
            </div>                
            <!--end::Top-->                

            <!--begin::Wrapper-->
            <div class="m-0"> 
              <!--begin::Label-->
              <div class="fw-bold fs-3 text-gray-800 mb-8">Quote #{{ quote?.quote_number || quote?.id?.slice(0, 8) }}</div>                
              <!--end::Label-->  

              <!--begin::Row-->
              <div class="row g-5 mb-11">
                <!--begin::Col-->
                <div class="col-sm-6">
                  <!--begin::Label-->
                  <div class="fw-semibold fs-7 text-gray-600 mb-1">Issue Date:</div>                
                  <!--end::Label-->  

                  <!--begin::Date-->
                  <div class="fw-bold fs-6 text-gray-800">{{ formatDate(quote?.created_on) }}</div>                
                  <!--end::Date-->  
                </div>                
                <!--end::Col-->  

                <!--begin::Col-->
                <div class="col-sm-6">
                  <!--begin::Label-->
                  <div class="fw-semibold fs-7 text-gray-600 mb-1">Valid Until:</div>                
                  <!--end::Label-->  

                  <!--begin::Info-->
                  <div class="fw-bold fs-6 text-gray-800 d-flex align-items-center flex-wrap">
                    <span class="pe-2">{{ getValidUntilDate() }}</span> 
                    
                    <span v-if="isExpiringSoon()" class="fs-7 text-warning d-flex align-items-center">
                      <span class="bullet bullet-dot bg-warning me-2"></span> 
                      Expires soon
                    </span>
                    <span v-else-if="isExpired()" class="fs-7 text-danger d-flex align-items-center">
                      <span class="bullet bullet-dot bg-danger me-2"></span> 
                      Expired
                    </span>
                  </div>                
                  <!--end::Info-->  
                </div>                
                <!--end::Col-->  
              </div>                
              <!--end::Row-->   

              <!--begin::Row-->
              <div class="row g-5 mb-12">
                <!--begin::Col-->
                <div class="col-sm-6">
                  <!--begin::Label-->
                  <div class="fw-semibold fs-7 text-gray-600 mb-1">Quote For:</div>                
                  <!--end::Label-->  

                  <!--begin::Customer Info-->
                  <div class="fw-bold fs-6 text-gray-800">{{ getCustomerName() }}</div>                
                  <!--end::Customer Info-->  

                  <!--begin::Description-->
                  <div class="fw-semibold fs-7 text-gray-600">
                    {{ getCustomerAddress() }}
                  </div>                
                  <!--end::Description-->
                  
                  <!--begin::Contact Info-->
                  <div class="fw-semibold fs-7 text-gray-600 mt-2">
                    <div v-if="quote?.contact?.email">Email: {{ quote.contact.email }}</div>
                    <div v-if="quote?.contact?.phone">Phone: {{ quote.contact.phone }}</div>
                  </div>
                  <!--end::Contact Info-->
                </div>                
                <!--end::Col-->  

                <!--begin::Col-->
                <div class="col-sm-6">
                  <!--begin::Label-->
                  <div class="fw-semibold fs-7 text-gray-600 mb-1">Issued By:</div>                
                  <!--end::Label-->  

                  <!--begin::Company Info-->
                  <div class="fw-bold fs-6 text-gray-800">JET ICU Medical Transport</div>                
                  <!--end::Company Info-->  

                  <!--begin::Address-->
                  <div class="fw-semibold fs-7 text-gray-600">                      
                    1511 N Westshore Blvd #650<br>
                    Tampa, FL 33607<br>
                    Phone: (352) 796-2540<br>
                    Email: info@jeticu.com                        
                  </div>                
                  <!--end::Address-->   
                </div>                
                <!--end::Col-->  
              </div>                
              <!--end::Row-->   

              <!--begin::Content-->
              <div class="flex-grow-1">
                <!--begin::Table-->
                <div class="table-responsive border-bottom mb-9">
                  <table class="table mb-3">
                    <thead>
                      <tr class="border-bottom fs-6 fw-bold text-muted">
                        <th class="min-w-175px pb-2">Service Description</th>
                        <th class="min-w-70px text-end pb-2">Distance</th>
                        <th class="min-w-80px text-end pb-2">Rate</th>
                        <th class="min-w-100px text-end pb-2">Amount</th>
                      </tr>
                    </thead>

                    <tbody>
                      <tr class="fw-bold text-gray-700 fs-5 text-end">
                        <td class="d-flex align-items-center pt-6">                                            
                          <div class="symbol symbol-40px symbol-circle me-3">
                            <img :src="getAircraftImage()" :alt="getAircraftTypeText()" class="symbol-label object-fit-cover" style="width: 40px; height: 40px; border-radius: 50%;" />
                          </div>                                        
                          Medical Air Transport
                          <div class="d-flex flex-column ms-3">
                            <span class="fs-7 text-muted">{{ getRouteInfo() }}</span>
                            <span class="fs-7 text-muted">{{ quote?.aircraft_type || 'Aircraft TBD' }}</span>
                          </div>
                        </td>
                        <td class="pt-6">{{ getDistanceDisplay() }}</td>
                        <td class="pt-6">${{ formatAmount(quote?.quoted_amount || 0) }}</td>
                        <td class="pt-6 text-gray-900 fw-bolder">${{ formatAmount(quote?.quoted_amount || 0) }}</td>
                      </tr>

                    </tbody>
                  </table>
                </div>  
                <!--end::Table-->                     

                <!--begin::Container-->
                <div class="d-flex justify-content-end">
                  <!--begin::Section-->
                  <div class="mw-300px">
                    <!--begin::Item-->
                    <div class="d-flex flex-stack mb-3">
                      <!--begin::Label-->
                      <div class="fw-semibold pe-10 text-gray-600 fs-7">Subtotal:</div>
                      <!--end::Label-->
                      <!--begin::Amount-->
                      <div class="text-end fw-bold fs-6 text-gray-800">${{ formatAmount(getSubtotal()) }}</div> 
                      <!--end::Amount-->
                    </div>
                    <!--end::Item-->

                    <!--begin::Item-->
                    <div class="d-flex flex-stack mb-3">
                      <!--begin::Label-->
                      <div class="fw-semibold pe-10 text-gray-600 fs-7">Tax (0%):</div>
                      <!--end::Label-->
                      <!--begin::Amount-->
                      <div class="text-end fw-bold fs-6 text-gray-800">$0.00</div> 
                      <!--end::Amount-->
                    </div>
                    <!--end::Item-->

                    <!--begin::Item-->
                    <div class="d-flex flex-stack mb-3">
                      <!--begin::Label-->
                      <div class="fw-semibold pe-10 text-gray-600 fs-7">Subtotal + Tax:</div>
                      <!--end::Label-->
                      <!--begin::Amount-->
                      <div class="text-end fw-bold fs-6 text-gray-800">${{ formatAmount(getSubtotal()) }}</div> 
                      <!--end::Amount-->
                    </div>
                    <!--end::Item-->

                    <!--begin::Item-->
                    <div class="d-flex flex-stack">
                      <!--begin::Label-->
                      <div class="fw-semibold pe-10 text-gray-600 fs-7">Total Amount:</div>
                      <!--end::Label-->
                      <!--begin::Total-->
                      <div class="text-end fw-bold fs-6 text-gray-800">${{ formatAmount(quote?.quoted_amount || 0) }}</div> 
                      <!--end::Total-->
                    </div>
                    <!--end::Item-->
                  </div>   
                  <!--end::Section-->                        
                </div>   
                <!--end::Container-->                 
              </div>
              <!--end::Content-->          
            </div>
            <!--end::Wrapper-->           
          </div>     
          <!--end::Quote content-->         
        </div>  
        <!--end::Content-->

        <!--begin::Sidebar-->
        <div class="m-0">
          <!--begin::Quote sidebar-->
          <div class="d-print-none border border-dashed border-gray-300 card-rounded h-lg-100 min-w-md-350px p-9 bg-lighten">
            <!--begin::Labels-->
            <div class="mb-8">       
              <div class="d-flex flex-column gap-2">
                <select 
                  v-if="quote?.status"
                  :value="quote.status"
                  @change="updateQuoteStatus(($event.target as HTMLSelectElement).value)"
                  class="form-select form-select-sm"
                  :class="`text-${getStatusColor(quote.status)}`"
                  style="max-width: 150px;"
                >
                  <option value="pending">Pending</option>
                  <option value="active">Active</option>
                  <option value="completed">Completed</option>
                  <option value="cancelled">Cancelled</option>
                </select>
                <span v-else class="badge badge-light-secondary">Draft</span>
                
                <select 
                  v-if="quote?.payment_status"
                  :value="quote.payment_status"
                  @change="updateQuotePaymentStatus(($event.target as HTMLSelectElement).value)"
                  class="form-select form-select-sm"
                  :class="`text-${getPaymentStatusColor(quote.payment_status)}`"
                  style="max-width: 150px;"
                >
                  <option value="pending">Payment Pending</option>
                  <option value="partial">Partial Paid</option>
                  <option value="paid">Paid</option>
                </select>
              </div>
          
            </div>                
            <!--end::Labels-->   
            
            <!--begin::Title-->
            <h6 class="mb-8 fw-bolder text-gray-600 text-hover-primary">QUOTE DETAILS</h6>
            <!--end::Title-->   

            <!--begin::Item-->
            <div class="mb-6">       
              <div class="fw-semibold text-gray-600 fs-7">Quote ID:</div> 
              <div class="fw-bold text-gray-800 fs-6">{{ quote?.quote_number || quote?.id?.slice(0, 8) }}</div>          
            </div>                
            <!--end::Item-->   

            <!--begin::Item-->
            <div class="mb-6">       
              <div class="fw-semibold text-gray-600 fs-7">Trip Type:</div> 
              <div class="fw-bold text-gray-800 fs-6">Medical Transport</div>          
            </div>                
            <!--end::Item-->  

            <!--begin::Item-->
            <div class="mb-15">     
              <div class="fw-semibold text-gray-600 fs-7">Valid For:</div>
              <div class="fw-bold fs-6 text-gray-800 d-flex align-items-center">
                {{ getValidityPeriod() }}
                <span v-if="isExpiringSoon()" class="fs-7 text-warning d-flex align-items-center">
                  <span class="bullet bullet-dot bg-warning mx-2"></span> 
                  Expires Soon
                </span>
                <span v-else-if="isExpired()" class="fs-7 text-danger d-flex align-items-center">
                  <span class="bullet bullet-dot bg-danger mx-2"></span> 
                  Expired
                </span>
              </div>                  
            </div>                
            <!--end::Item-->  

            <!--begin::Title-->
            <h6 class="mb-8 fw-bolder text-gray-600 text-hover-primary">PATIENT DETAILS</h6>
            <!--end::Title-->   

            <!--begin::Item-->
            <div class="mb-6">     
              <div class="fw-semibold text-gray-600 fs-7">Patient Name:</div>
              <div class="fw-bold fs-6 text-gray-800">
                {{ getPatientName() }}
                <a v-if="quote?.patient_id" 
                   href="#" 
                   @click.prevent="viewPatient" 
                   class="link-primary ps-1">
                  View Profile
                </a>
              </div>                  
            </div>                
            <!--end::Item-->  

 

            <!--begin::Title-->
            <h6 class="mb-8 fw-bolder text-gray-600 text-hover-primary">FLIGHT DETAILS</h6>
            <!--end::Title-->   

            <!--begin::Item-->
            <div class="mb-6">     
              <div class="fw-semibold text-gray-600 fs-7">Route:</div>
              <div class="fw-bold fs-6 text-gray-800">{{ getRouteInfo() }}</div>                  
            </div>                
            <!--end::Item-->  

            <!--begin::Item-->
            <div class="mb-6">       
              <div class="fw-semibold text-gray-600 fs-7">Aircraft Type:</div> 
              <div class="fw-bold text-gray-800 fs-6">
                <template v-if="quote?.aircraft_type && quote.aircraft_type !== 'TBD'">
                  <span v-if="quote.aircraft_type === '65'">Learjet 65</span>
                  <span v-else-if="quote.aircraft_type === '35'">Learjet 35</span>
                  <span v-else>{{ quote.aircraft_type }}</span>
                </template>
                <template v-else>
                  TBD
                </template>
              </div>          
            </div>                
            <!--end::Item-->  

            <!--begin::Item-->
            <div class="m-0">     
              <div class="fw-semibold text-gray-600 fs-7">Estimated Flight Time:</div>
              <div class="fw-bold fs-6 text-gray-800 d-flex align-items-center">
                {{ getEstimatedFlightTime() }}
                <span class="fs-7 text-success d-flex align-items-center">
                  <span class="bullet bullet-dot bg-success mx-2"></span> 
                  {{ getDistanceDisplay() }}
                </span>
              </div>                  
            </div>                
            <!--end::Item-->  
          </div>                
          <!--end::Quote sidebar-->                  
        </div>  
        <!--end::Sidebar-->
      </div>
      <!--end::Layout-->         
    </div>
    <!--end::Body-->
  </div>
  
  <!-- Updates Timeline -->
  <UpdatesTimeline 
    v-if="quote?.id"
    entity-type="quote"
    :entity-id="quote.id"
    :allow-comments="true"
    :entity-data="quote"
  />
  
  <!-- Include the Create Trip Modal -->
  <CreateTripMultiStepModal @tripCreated="onTripCreated" />
  
  <!-- Email Quote Modal -->
  <div 
    class="modal fade" 
    id="kt_modal_email_quote" 
    tabindex="-1" 
    aria-hidden="true"
    ref="emailModalRef"
  >
    <div class="modal-dialog modal-dialog-centered mw-650px">
      <div class="modal-content">
        <div class="modal-header">
          <h2 class="fw-bold">Email Quote</h2>
          <div 
            class="btn btn-icon btn-sm btn-active-icon-primary" 
            data-bs-dismiss="modal"
          >
            <KTIcon icon-name="cross" icon-class="fs-1" />
          </div>
        </div>
        
        <div class="modal-body scroll-y mx-5 mx-xl-15 my-7">
          <form @submit.prevent="sendEmailQuote">
            <!-- Email Address -->
            <div class="fv-row mb-7">
              <label class="required fw-semibold fs-6 mb-2">Email Address</label>
              <input
                v-model="emailForm.email"
                type="email"
                class="form-control form-control-solid mb-3 mb-lg-0"
                placeholder="Enter email address"
                required
              />
            </div>
            
            <!-- Subject -->
            <div class="fv-row mb-7">
              <label class="fw-semibold fs-6 mb-2">Subject</label>
              <input
                v-model="emailForm.subject"
                type="text"
                class="form-control form-control-solid mb-3 mb-lg-0"
                placeholder="Quote from JET ICU Medical Transport"
              />
            </div>
            
            <!-- Message -->
            <div class="fv-row mb-7">
              <label class="fw-semibold fs-6 mb-2">Message (Optional)</label>
              <textarea
                v-model="emailForm.message"
                class="form-control form-control-solid"
                rows="4"
                placeholder="Add a personal message..."
              ></textarea>
            </div>
            
            <!-- Include PDF -->
            <div class="fv-row mb-7">
              <div class="form-check">
                <input
                  v-model="emailForm.includePdf"
                  class="form-check-input"
                  type="checkbox"
                  id="includePdf"
                />
                <label class="form-check-label fw-semibold text-gray-700" for="includePdf">
                  Include PDF attachment
                </label>
              </div>
            </div>
          </form>
        </div>
        
        <div class="modal-footer">
          <button 
            type="button" 
            class="btn btn-light" 
            data-bs-dismiss="modal"
          >
            Cancel
          </button>
          <button 
            type="button" 
            class="btn btn-primary" 
            @click="sendEmailQuote"
            :disabled="!emailForm.email || isEmailSending"
          >
            <span v-if="isEmailSending" class="spinner-border spinner-border-sm me-2"></span>
            {{ isEmailSending ? 'Sending...' : 'Send Email' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from "vue";
import { useRoute, useRouter } from "vue-router";
import ApiService from "@/core/services/ApiService";
import Swal from "sweetalert2";
import { useToolbar, createToolbarActions } from "@/core/helpers/toolbar";
import { Modal } from "bootstrap";
import CreateTripMultiStepModal from "@/components/modals/CreateTripMultiStepModal.vue";
import UpdatesTimeline from "@/components/UpdatesTimeline.vue";
import JwtService from "@/core/services/JwtService";

const route = useRoute();
const router = useRouter();
const quote = ref<any>(null);
const associatedTrip = ref<any>(null);
const loading = ref(true);
const tripLoading = ref(false);
const error = ref<string | null>(null);
const { setToolbarActions } = useToolbar();

// Email modal refs and form data
const emailModalRef = ref<HTMLElement | null>(null);
const isEmailSending = ref(false);
const emailForm = ref({
  email: '',
  subject: '',
  message: '',
  includePdf: true
});

const fetchQuote = async () => {
  try {
    loading.value = true;
    error.value = null;
    associatedTrip.value = null; // Reset associated trip before fetching
    const quoteId = route.params.id as string;
    
    const response = await ApiService.get(`/quotes/${quoteId}/`);
    quote.value = response.data;
    
    // Check if there's a trip associated with this quote
    checkForAssociatedTrip();
    
    // Setup toolbar actions after quote is loaded and trip check is done
    setupToolbarActions();
    
  } catch (err: any) {
    error.value = err.response?.data?.detail || "Failed to fetch quote details";
    console.error("Error fetching quote:", err);
  } finally {
    loading.value = false;
  }
};

const checkForAssociatedTrip = () => {
  // Use trips data directly from the quote response
  if (quote.value?.trips && Array.isArray(quote.value.trips) && quote.value.trips.length > 0) {
    associatedTrip.value = quote.value.trips[0]; // Take the first trip
    console.log('Found associated trip:', associatedTrip.value.id);
  } else {
    associatedTrip.value = null;
    console.log('No associated trips found for this quote');
  }
};


const setupToolbarActions = () => {
  const actions = [];
  
  // Build dropdown items conditionally
  const dropdownItems = [];
  
  // Only show Edit Quote if there's no associated trip
  if (!associatedTrip.value) {
    dropdownItems.push({
      id: 'edit-quote',
      label: 'Edit Quote',
      icon: 'pencil',
      handler: editQuote
    });
  }
  
  // Always show these options
  dropdownItems.push(
    {
      id: 'download-pdf',
      label: 'Download PDF',
      icon: 'document',
      handler: downloadQuote
    },
    {
      id: 'email-quote',
      label: 'Email Quote',
      icon: 'sms',
      handler: emailQuote
    }
  );
  
  // Add divider and delete option
  dropdownItems.push(
    { divider: true },
    {
      id: 'delete-quote',
      label: 'Delete Quote',
      icon: 'trash',
      handler: deleteQuote,
      className: 'text-danger'
    }
  );
  
  // Add Actions dropdown
  actions.push({
    id: 'quote-actions-dropdown',
    label: 'Actions',
    variant: 'dark',
    isDropdown: true,
    dropdownItems: dropdownItems
  });
  
  // Add Convert to Trip button only if quote hasn't been converted yet
  if (!associatedTrip.value) {
    actions.push(
      createToolbarActions.primary('convert-to-trip', 'Convert to Trip', openConvertToTripModal, 'airplane')
    );
  }
  
  setToolbarActions(actions);
};

const formatDate = (dateString?: string): string => {
  if (!dateString) return 'N/A';
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
};

const formatAmount = (amount: number): string => {
  return new Intl.NumberFormat('en-US', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(amount);
};

const getCustomerName = (): string => {
  if (quote.value?.contact) {
    const first = quote.value.contact.first_name || '';
    const last = quote.value.contact.last_name || '';
    return `${first} ${last}`.trim() || quote.value.contact.email || 'Customer';
  }
  return 'Customer Name Not Available';
};

const getPatientName = (): string => {
  // First check if there's a related patient object with patient info
  if (quote.value?.patient?.info) {
    const first = quote.value.patient.info.first_name || '';
    const last = quote.value.patient.info.last_name || '';
    const fullName = `${first} ${last}`.trim();
    return fullName || quote.value.patient.info.email || 'Patient';
  }
  
  // If patient exists but no info, show basic info
  if (quote.value?.patient) {
    return `Patient (ID: ${quote.value.patient.id.slice(0, 8)})`;
  }
  
  return 'No Patient Assigned';
};

const getCustomerAddress = (): string => {
  if (!quote.value?.contact) return 'Address not available';
  
  const contact = quote.value.contact;
  const parts = [
    contact.address,
    contact.city,
    contact.state,
    contact.zip_code,
    contact.country
  ].filter(Boolean);
  
  return parts.length > 0 ? parts.join(', ') : 'Address not available';
};

const getRouteInfo = (): string => {
  const pickupAirport = quote.value?.pickup_airport;
  const dropoffAirport = quote.value?.dropoff_airport;
  
  if (pickupAirport?.ident && dropoffAirport?.ident) {
    return `${pickupAirport.ident} → ${dropoffAirport.ident}`;
  }
  return 'Route TBD';
};

const getBaseAmount = (): number => {
  return quote.value?.quoted_amount || 0;
};


const getSubtotal = (): number => {
  return quote.value?.quoted_amount || 0;
};

const getTaxRate = (): number => {
  return 0;
};

const getTaxAmount = (): number => {
  return 0;
};

const getStatusColor = (status: string): string => {
  switch (status?.toLowerCase()) {
    case 'active': case 'completed': return 'success';
    case 'pending': return 'warning';
    case 'cancelled': return 'danger';
    case 'sent': return 'primary';
    case 'draft': return 'secondary';
    default: return 'info';
  }
};

const getPaymentStatusColor = (paymentStatus: string): string => {
  switch (paymentStatus?.toLowerCase()) {
    case 'paid': return 'success';
    case 'partial': return 'warning';
    case 'pending': return 'danger';
    default: return 'secondary';
  }
};

const getContentTypeId = (entityType: string): number => {
  // Map entity types to content type IDs
  const contentTypeMap: Record<string, number> = {
    'quote': 22,
    'trip': 23,
    'patient': 17,
    'contact': 9,
    'passenger': 18,
    'aircraft': 15,
    'fbo': 10,
    // Add more mappings as needed
  };
  return contentTypeMap[entityType] || 1;
};

const isExpired = (): boolean => {
  if (!quote.value?.created_on) return false;
  const issueDate = new Date(quote.value.created_on);
  const validUntil = new Date(issueDate.getTime() + 30 * 24 * 60 * 60 * 1000);
  return validUntil < new Date();
};

const isExpiringSoon = (): boolean => {
  if (!quote.value?.created_on) return false;
  const issueDate = new Date(quote.value.created_on);
  const validUntil = new Date(issueDate.getTime() + 30 * 24 * 60 * 60 * 1000);
  const threeDaysFromNow = new Date();
  threeDaysFromNow.setDate(threeDaysFromNow.getDate() + 3);
  return validUntil <= threeDaysFromNow && validUntil >= new Date();
};

const getValidUntilDate = (): string => {
  if (!quote.value?.created_on) return formatDate(new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString());
  
  const issueDate = new Date(quote.value.created_on);
  const validUntil = new Date(issueDate.getTime() + 30 * 24 * 60 * 60 * 1000);
  return formatDate(validUntil.toISOString());
};

const getValidityPeriod = (): string => {
  return '30 days';
};

const calculateDistance = (lat1: number, lon1: number, lat2: number, lon2: number): number => {
  const R = 3959; // Earth's radius in miles
  const dLat = (lat2 - lat1) * Math.PI / 180;
  const dLon = (lon2 - lon1) * Math.PI / 180;
  const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
    Math.sin(dLon / 2) * Math.sin(dLon / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  const distance = R * c;
  return Math.round(distance);
};

const getDistanceDisplay = (): string => {
  const pickupAirport = quote.value?.pickup_airport;
  const dropoffAirport = quote.value?.dropoff_airport;
  
  if (pickupAirport?.latitude && pickupAirport?.longitude && 
      dropoffAirport?.latitude && dropoffAirport?.longitude) {
    const distance = calculateDistance(
      pickupAirport.latitude, pickupAirport.longitude,
      dropoffAirport.latitude, dropoffAirport.longitude
    );
    return `${distance} mi`;
  }
  return 'TBD';
};

const getEstimatedFlightTime = (): string => {
  const pickupAirport = quote.value?.pickup_airport;
  const dropoffAirport = quote.value?.dropoff_airport;
  
  if (pickupAirport?.latitude && pickupAirport?.longitude && 
      dropoffAirport?.latitude && dropoffAirport?.longitude) {
    const distance = calculateDistance(
      pickupAirport.latitude, pickupAirport.longitude,
      dropoffAirport.latitude, dropoffAirport.longitude
    );
    
    // Calculate flight time based on average speed of 400 mph
    const hours = distance / 400;
    const flightHours = Math.floor(hours);
    const flightMinutes = Math.round((hours - flightHours) * 60);
    
    if (flightHours > 0) {
      return `${flightHours}h ${flightMinutes}m`;
    } else {
      return `${flightMinutes}m`;
    }
  }
  
  return 'TBD';
};

const openConvertToTripModal = () => {
  // Get the modal element and show it with pre-populated data
  const modalElement = document.getElementById('kt_modal_create_trip_multistep');
  if (modalElement) {
    console.log('Opening Convert to Trip modal with quote:', quote.value);
    // Dispatch custom event with quote data for pre-population
    const eventData = {
      quoteId: quote.value?.id,
      tripType: 'medical', // Default to medical for quote conversions
      patientId: quote.value?.patient?.id,
      departureAirport: quote.value?.pickup_airport?.id,
      arrivalAirport: quote.value?.dropoff_airport?.id,
      notes: `Converted from Quote #${quote.value?.id?.slice(0, 8)}\n\nQuote Details:\n- Aircraft Type: ${quote.value?.aircraft_type || 'TBD'}\n- Medical Team: ${quote.value?.medical_team || 'TBD'}\n- Quoted Amount: $${quote.value?.quoted_amount || 'TBD'}`,
      // Include additional quote info for reference
      quoteData: {
        aircraftType: quote.value?.aircraft_type,
        medicalTeam: quote.value?.medical_team,
        quotedAmount: quote.value?.quoted_amount,
        estimatedFlightTime: quote.value?.estimated_flight_time,
        includesGrounds: quote.value?.includes_grounds,
        numberOfStops: quote.value?.number_of_stops
      }
    };
    console.log('Sending pre-populate data:', eventData);
    const event = new CustomEvent('prepopulate-trip-form', {
      detail: eventData
    });
    modalElement.dispatchEvent(event);
    
    const modal = new Modal(modalElement);
    modal.show();
  } else {
    console.error('Could not find modal element kt_modal_create_trip_multistep');
  }
};

const downloadQuote = async () => {
  if (!quote.value?.id) {
    Swal.fire({
      title: 'Error',
      text: 'Quote not found',
      icon: 'error',
      confirmButtonText: 'OK'
    });
    return;
  }

  try {
    // Show loading indicator
    Swal.fire({
      title: 'Generating PDF...',
      text: 'Please wait while we prepare your quote PDF.',
      allowOutsideClick: false,
      showConfirmButton: false,
      willOpen: () => {
        Swal.showLoading();
      }
    });

    // Call the PDF endpoint using fetch for blob response
    const baseURL = import.meta.env.VITE_APP_API_URL || "http://localhost:8001/api";
    const token = JwtService.getToken();
    
    const response = await fetch(`${baseURL}/quotes/${quote.value.id}/pdf/`, {
      method: 'GET',
      headers: {
        'Authorization': token ? `Bearer ${token}` : '',
      }
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const blob = await response.blob();

    // Close loading dialog
    Swal.close();

    // Create download link
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `quote_${quote.value.id.slice(0, 8)}.pdf`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    // Clean up the URL
    window.URL.revokeObjectURL(url);

    // Show success message
    Swal.fire({
      title: 'Success!',
      text: 'Quote PDF has been downloaded.',
      icon: 'success',
      confirmButtonText: 'OK'
    });

  } catch (error: any) {
    console.error('Error downloading PDF:', error);
    Swal.fire({
      title: 'Error!',
      text: error.response?.data?.detail || 'Failed to download PDF. Please try again.',
      icon: 'error',
      confirmButtonText: 'OK'
    });
  }
};

const editQuote = () => {
  if (!quote.value) return;
  router.push(`/admin/quotes/${quote.value.id}/edit`);
};

const viewPatient = () => {
  if (quote.value?.patient_id) {
    router.push(`/admin/contacts/patients/${quote.value.patient_id}`);
  }
};

const updateQuoteStatus = async (newStatus: string) => {
  if (!quote.value || quote.value.status === newStatus) return;
  
  // If changing to cancelled, prompt for cancellation reason
  if (newStatus === 'cancelled') {
    const result = await Swal.fire({
      title: 'Quote Cancellation',
      text: 'Please enter a reason for cancellation:',
      input: 'textarea',
      inputPlaceholder: 'Enter cancellation reason...',
      inputAttributes: {
        'aria-label': 'Cancellation reason',
        'style': 'min-height: 100px;'
      },
      showCancelButton: true,
      confirmButtonText: 'Cancel Quote',
      cancelButtonText: 'Keep Current Status',
      confirmButtonColor: '#dc3545',
      inputValidator: (value) => {
        if (!value || value.trim().length === 0) {
          return 'Please enter a reason for cancellation';
        }
        if (value.trim().length < 10) {
          return 'Please provide a more detailed reason (at least 10 characters)';
        }
      }
    });

    if (!result.isConfirmed) {
      // User cancelled, force reactive update to reset dropdown
      const currentStatus = quote.value.status;
      quote.value.status = '';
      nextTick(() => {
        quote.value.status = currentStatus;
      });
      return;
    }

    // Save the cancellation reason as a comment
    try {
      await ApiService.post('/comments/', {
        content_type: getContentTypeId('quote'),
        object_id: quote.value.id,
        text: `Quote cancelled: ${result.value.trim()}`
      });
    } catch (error) {
      console.error('Error saving cancellation comment:', error);
      // Continue with status update even if comment fails
    }
  }
  
  try {
    await ApiService.patch(`/quotes/${quote.value.id}/`, { status: newStatus });
    
    // Update the local quote status
    quote.value.status = newStatus;
    
    // Show success notification
    Swal.fire({
      title: "Status Updated!",
      text: `Quote status changed to ${newStatus}`,
      icon: "success",
      timer: 2000,
      showConfirmButton: false
    });
    
    // Refresh toolbar actions in case they depend on status
    setupToolbarActions();
    
  } catch (error: any) {
    console.error('Error updating quote status:', error);
    Swal.fire({
      title: 'Error!',
      text: error.response?.data?.detail || 'Failed to update status. Please try again.',
      icon: 'error',
      confirmButtonText: 'OK'
    });
  }
};

const updateQuotePaymentStatus = async (newPaymentStatus: string) => {
  if (!quote.value || quote.value.payment_status === newPaymentStatus) return;
  
  try {
    await ApiService.patch(`/quotes/${quote.value.id}/`, { payment_status: newPaymentStatus });
    
    // Update the local quote payment status
    quote.value.payment_status = newPaymentStatus;
    
    // Show success notification
    Swal.fire({
      title: "Payment Status Updated!",
      text: `Payment status changed to ${newPaymentStatus}`,
      icon: "success",
      timer: 2000,
      showConfirmButton: false
    });
    
  } catch (error: any) {
    console.error('Error updating quote payment status:', error);
    Swal.fire({
      title: 'Error!',
      text: error.response?.data?.detail || 'Failed to update payment status. Please try again.',
      icon: 'error',
      confirmButtonText: 'OK'
    });
  }
};

// Handle trip creation success
const onTripCreated = async (tripData: any) => {
  console.log('Trip created from quote:', tripData);
  
  // Update quote status to active
  if (quote.value && quote.value.id) {
    try {
      // Update the quote status to 'active' since it's been converted to a trip
      const updateData = {
        status: 'active'
      };
      
      console.log('Updating quote status to active:', quote.value.id);
      await ApiService.patch(`/quotes/${quote.value.id}/`, updateData);
      
      // Update local quote object
      quote.value.status = 'active';
      
      // Set the associated trip data to show the trip card
      associatedTrip.value = tripData;
      
      setupToolbarActions(); // Refresh toolbar to hide Convert button
      
      console.log('Quote status updated successfully');
    } catch (error) {
      console.error('Error updating quote status:', error);
      // Still show success for trip creation even if quote update fails
    }
  }
  
  // Show success message with option to view the trip
  Swal.fire({
    title: 'Quote Converted!',
    text: `Quote has been successfully converted to Trip ${tripData.trip_number}`,
    icon: 'success',
    showCancelButton: true,
    confirmButtonText: 'View Trip',
    cancelButtonText: 'Stay Here'
  }).then((result) => {
    if (result.isConfirmed) {
      router.push(`/admin/trips/${tripData.id}`);
    } else {
      // If staying, refresh the quote to show updated status
      fetchQuote();
    }
  });
};

// Helper functions for trip display
const getTripStatusColor = (status: string): string => {
  switch (status?.toLowerCase()) {
    case 'pending': return 'warning';
    case 'active': case 'in_progress': return 'primary';
    case 'completed': return 'success';
    case 'cancelled': return 'danger';
    case 'scheduled': return 'info';
    default: return 'secondary';
  }
};

// Removed getTripPatientName - using existing getPatientName() instead

const viewTrip = () => {
  if (associatedTrip.value?.id) {
    router.push(`/admin/trips/${associatedTrip.value.id}`);
  }
};

// Aircraft image helper functions
const getAircraftImage = (): string => {
  const aircraftType = quote.value?.aircraft_type;
  if (!aircraftType || aircraftType === 'TBD') return '/media/aircraft/Learjet35A.jpg';
  
  // Map aircraft types to their image filenames
  const imageMap: Record<string, string> = {
    '35': 'Learjet35A.jpg',
    '36A': 'learjet36a.jpeg', 
    '31': 'learjet30.jpg',
    '60': 'Learjet60.jpg',
    'Kodiak 100': 'kodiak100.jpg',
    'Learjet 35A': 'Learjet35A.jpg',
    'Learjet 36A': 'learjet36a.jpeg',
    'Learjet 31': 'learjet30.jpg',
    'Learjet 60': 'Learjet60.jpg',
  };
  
  // Return specific image or fallback to generic
  const imageName = imageMap[aircraftType] || 'Learjet35A.jpg'; // Default fallback
  return `/media/aircraft/${imageName}`;
};

const getAircraftTypeText = (): string => {
  const aircraftType = quote.value?.aircraft_type;
  if (!aircraftType || aircraftType === 'TBD') return 'Aircraft TBD';
  
  // Convert numeric codes to full names
  const typeMap: Record<string, string> = {
    '35': 'Learjet 35A',
    '36A': 'Learjet 36A',
    '31': 'Learjet 31', 
    '60': 'Learjet 60',
  };
  
  return typeMap[aircraftType] || aircraftType;
};

// Additional action handlers for dropdown menu
const emailQuote = () => {
  // Pre-fill form data
  emailForm.value.email = quote.value?.contact?.email || '';
  emailForm.value.subject = `Quote #${quote.value?.id?.slice(0, 8)} from JET ICU Medical Transport`;
  emailForm.value.message = `Dear ${quote.value?.contact?.first_name || 'Customer'},\n\nPlease find your transportation quote attached.\n\nBest regards,\nJET ICU Medical Transport Team`;
  emailForm.value.includePdf = true;
  
  // Open modal
  const modalElement = document.getElementById('kt_modal_email_quote');
  if (modalElement) {
    const modal = new Modal(modalElement);
    modal.show();
  }
};

const sendEmailQuote = async () => {
  if (!emailForm.value.email.trim()) {
    Swal.fire({
      title: 'Error',
      text: 'Please enter an email address.',
      icon: 'error',
      confirmButtonText: 'OK'
    });
    return;
  }
  
  isEmailSending.value = true;
  
  try {
    // TODO: Replace with actual email API call when backend email service is ready
    const emailData = {
      quote_id: quote.value?.id,
      to_email: emailForm.value.email,
      subject: emailForm.value.subject,
      message: emailForm.value.message,
      include_pdf: emailForm.value.includePdf
    };
    
    console.log('Email data prepared for backend API:', emailData);
    console.log('PDF endpoint available at: /quotes/' + quote.value?.id + '/pdf/');
    
    // Simulate API call (replace with: await ApiService.post('/quotes/email/', emailData))
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // Close modal
    const modalElement = document.getElementById('kt_modal_email_quote');
    if (modalElement) {
      const modal = Modal.getInstance(modalElement);
      modal?.hide();
    }
    
    // Show success message
    Swal.fire({
      title: 'Email Sent!',
      text: `Quote has been sent to ${emailForm.value.email}`,
      icon: 'success',
      confirmButtonText: 'OK'
    });
    
    // Reset form
    emailForm.value.email = '';
    emailForm.value.subject = '';
    emailForm.value.message = '';
    emailForm.value.includePdf = true;
    
  } catch (error) {
    console.error('Error sending email:', error);
    Swal.fire({
      title: 'Error!',
      text: 'Failed to send email. Please try again.',
      icon: 'error',
      confirmButtonText: 'OK'
    });
  } finally {
    isEmailSending.value = false;
  }
};

const deleteQuote = () => {
  if (!quote.value) return;
  
  Swal.fire({
    title: 'Delete Quote',
    text: 'Are you sure you want to delete this quote? This action cannot be undone.',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonText: 'Yes, Delete',
    cancelButtonText: 'Cancel',
    confirmButtonColor: '#d33'
  }).then(async (result) => {
    if (result.isConfirmed) {
      try {
        await ApiService.delete(`/quotes/${quote.value!.id}/`);
        
        Swal.fire({
          title: 'Deleted!',
          text: 'Quote has been deleted successfully.',
          icon: 'success',
          confirmButtonText: 'OK'
        }).then(() => {
          router.push('/admin/quotes');
        });
      } catch (error) {
        console.error('Error deleting quote:', error);
        Swal.fire({
          title: 'Error!',
          text: 'Failed to delete the quote. Please try again.',
          icon: 'error',
          confirmButtonText: 'OK'
        });
      }
    }
  });
};

onMounted(() => {
  fetchQuote();
});
</script>