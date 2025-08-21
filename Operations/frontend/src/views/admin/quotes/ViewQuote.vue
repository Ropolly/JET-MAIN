<template>
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
                <button 
                  v-if="!quote?.trip_id" 
                  @click="convertToTrip" 
                  class="btn btn-sm btn-success"
                >
                  <KTIcon icon-name="airplane" icon-class="fs-3" />
                  Convert to Trip
                </button>
                <a href="#" @click="downloadQuote" class="btn btn-sm btn-primary">
                  <KTIcon icon-name="document" icon-class="fs-3" />
                  Download PDF
                </a>
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
                    <span class="pe-2">{{ formatDate(quote?.valid_until) }}</span> 
                    
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
                    <div v-if="quote?.customer?.email">Email: {{ quote.customer.email }}</div>
                    <div v-if="quote?.customer?.phone">Phone: {{ quote.customer.phone }}</div>
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
                    1234 Aviation Blvd<br>
                    Los Angeles, CA 90045<br>
                    Phone: (555) 123-4567<br>
                    Email: quotes@jeticumedical.com                        
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
                          <KTIcon icon-name="airplane" icon-class="fs-2 text-primary me-3" />                                           
                          Medical Air Transport
                          <div class="d-flex flex-column ms-3">
                            <span class="fs-7 text-muted">{{ getRouteInfo() }}</span>
                            <span class="fs-7 text-muted">{{ quote?.aircraft_type || 'Aircraft TBD' }}</span>
                          </div>
                        </td>
                        <td class="pt-6">{{ quote?.distance || 0 }} mi</td>
                        <td class="pt-6">${{ getBaseRate() }}</td>
                        <td class="pt-6 text-gray-900 fw-bolder">${{ formatAmount(getBaseAmount()) }}</td>
                      </tr>

                      <tr v-if="getMedicalTeamCost() > 0" class="fw-bold text-gray-700 fs-5 text-end">
                        <td class="d-flex align-items-center">                                           
                          <KTIcon icon-name="cross" icon-class="fs-2 text-danger me-3" />                                        
                          Medical Team & Equipment
                          <div class="ms-3">
                            <span class="fs-7 text-muted">{{ quote?.medical_team || 'Standard medical crew' }}</span>
                          </div>
                        </td>
                        <td>-</td>
                        <td>${{ getMedicalTeamRate() }}</td>
                        <td class="fs-5 text-gray-900 fw-bolder">${{ formatAmount(getMedicalTeamCost()) }}</td>
                      </tr>
                      
                      <tr v-if="getGroundTransportCost() > 0" class="fw-bold text-gray-700 fs-5 text-end">
                        <td class="d-flex align-items-center">                                           
                          <KTIcon icon-name="truck" icon-class="fs-2 text-success me-3" />                                          
                          Ground Transportation
                          <div class="ms-3">
                            <span class="fs-7 text-muted">Airport transfers and ground support</span>
                          </div>
                        </td>
                        <td>-</td>
                        <td>$150.00</td>
                        <td class="fs-5 text-gray-900 fw-bolder">${{ formatAmount(getGroundTransportCost()) }}</td>
                      </tr>

                      <tr v-if="getAdditionalServices() > 0" class="fw-bold text-gray-700 fs-5 text-end">
                        <td class="d-flex align-items-center">                                           
                          <KTIcon icon-name="add-item" icon-class="fs-2 text-info me-3" />                                          
                          Additional Services
                          <div class="ms-3">
                            <span class="fs-7 text-muted">Special accommodations and extras</span>
                          </div>
                        </td>
                        <td>-</td>
                        <td>Variable</td>
                        <td class="fs-5 text-gray-900 fw-bolder">${{ formatAmount(getAdditionalServices()) }}</td>
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
                      <div class="fw-semibold pe-10 text-gray-600 fs-7">Tax ({{ getTaxRate() }}%):</div>
                      <!--end::Label-->
                      <!--begin::Amount-->
                      <div class="text-end fw-bold fs-6 text-gray-800">${{ formatAmount(getTaxAmount()) }}</div> 
                      <!--end::Amount-->
                    </div>
                    <!--end::Item-->

                    <!--begin::Item-->
                    <div class="d-flex flex-stack mb-3">
                      <!--begin::Label-->
                      <div class="fw-semibold pe-10 text-gray-600 fs-7">Subtotal + Tax:</div>
                      <!--end::Label-->
                      <!--begin::Amount-->
                      <div class="text-end fw-bold fs-6 text-gray-800">${{ formatAmount(getSubtotal() + getTaxAmount()) }}</div> 
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
              <span :class="`badge badge-light-${getStatusColor(quote?.status)} me-2`">
                {{ quote?.status || 'Draft' }}
              </span> 
              <span v-if="quote?.trip_id" class="badge badge-light-success">
                Converted to Trip
              </span>
              <span v-else class="badge badge-light-warning">
                Pending Conversion
              </span>          
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
              <div class="fw-bold text-gray-800 fs-6">{{ quote?.trip_type || 'Medical Transport' }}</div>          
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
                   @click="viewPatient" 
                   class="link-primary ps-1">
                  View Profile
                </a>
              </div>                  
            </div>                
            <!--end::Item-->  

            <!--begin::Item-->
            <div class="mb-6">       
              <div class="fw-semibold text-gray-600 fs-7">Medical Condition:</div> 
              <div class="fw-bold text-gray-800 fs-6">{{ quote?.medical_condition || 'Not specified' }}</div>          
            </div>                
            <!--end::Item-->  

            <!--begin::Item-->
            <div class="mb-6">       
              <div class="fw-semibold text-gray-600 fs-7">Special Requirements:</div> 
              <div class="fw-bold text-gray-800 fs-6">{{ quote?.special_requirements || 'None' }}</div>          
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
              <div class="fw-bold text-gray-800 fs-6">{{ quote?.aircraft_type || 'TBD' }}</div>          
            </div>                
            <!--end::Item-->  

            <!--begin::Item-->
            <div class="m-0">     
              <div class="fw-semibold text-gray-600 fs-7">Estimated Flight Time:</div>
              <div class="fw-bold fs-6 text-gray-800 d-flex align-items-center">
                {{ getEstimatedFlightTime() }}
                <span class="fs-7 text-success d-flex align-items-center">
                  <span class="bullet bullet-dot bg-success mx-2"></span> 
                  {{ quote?.distance || 0 }} miles
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
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import ApiService from "@/core/services/ApiService";
import Swal from "sweetalert2";

const route = useRoute();
const router = useRouter();
const quote = ref<any>(null);
const loading = ref(true);
const error = ref<string | null>(null);

const fetchQuote = async () => {
  try {
    loading.value = true;
    error.value = null;
    const quoteId = route.params.id as string;
    
    const response = await ApiService.get(`/quotes/${quoteId}/`);
    quote.value = response.data;
    
  } catch (err: any) {
    error.value = err.response?.data?.detail || "Failed to fetch quote details";
    console.error("Error fetching quote:", err);
  } finally {
    loading.value = false;
  }
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
  if (quote.value?.customer) {
    const first = quote.value.customer.first_name || '';
    const last = quote.value.customer.last_name || '';
    return `${first} ${last}`.trim() || quote.value.customer.email || 'Customer';
  }
  if (quote.value?.patient_first_name || quote.value?.patient_last_name) {
    return `${quote.value.patient_first_name || ''} ${quote.value.patient_last_name || ''}`.trim();
  }
  return 'Customer Name Not Available';
};

const getPatientName = (): string => {
  if (quote.value?.patient) {
    const first = quote.value.patient.first_name || '';
    const last = quote.value.patient.last_name || '';
    return `${first} ${last}`.trim() || 'Patient';
  }
  if (quote.value?.patient_first_name || quote.value?.patient_last_name) {
    return `${quote.value.patient_first_name || ''} ${quote.value.patient_last_name || ''}`.trim();
  }
  return 'Patient Name Not Specified';
};

const getCustomerAddress = (): string => {
  if (!quote.value?.customer) return 'Address not available';
  
  const customer = quote.value.customer;
  const parts = [
    customer.address,
    customer.city,
    customer.state,
    customer.zip_code,
    customer.country
  ].filter(Boolean);
  
  return parts.length > 0 ? parts.join(', ') : 'Address not available';
};

const getRouteInfo = (): string => {
  const pickup = quote.value?.pickup_airport_id || quote.value?.departure_airport;
  const dropoff = quote.value?.dropoff_airport_id || quote.value?.arrival_airport;
  
  if (pickup && dropoff) {
    return `${pickup} → ${dropoff}`;
  }
  return 'Route TBD';
};

const getBaseAmount = (): number => {
  return quote.value?.base_amount || (quote.value?.quoted_amount * 0.7) || 0;
};

const getBaseRate = (): string => {
  const distance = quote.value?.distance || 1;
  const baseAmount = getBaseAmount();
  const rate = baseAmount / distance;
  return formatAmount(rate);
};

const getMedicalTeamCost = (): number => {
  return quote.value?.medical_team_cost || (quote.value?.quoted_amount * 0.2) || 0;
};

const getMedicalTeamRate = (): string => {
  return formatAmount(getMedicalTeamCost());
};

const getGroundTransportCost = (): number => {
  return quote.value?.ground_transport_cost || 150;
};

const getAdditionalServices = (): number => {
  return quote.value?.additional_services_cost || 0;
};

const getSubtotal = (): number => {
  return getBaseAmount() + getMedicalTeamCost() + getGroundTransportCost() + getAdditionalServices();
};

const getTaxRate = (): number => {
  return quote.value?.tax_rate || 8.25;
};

const getTaxAmount = (): number => {
  return getSubtotal() * (getTaxRate() / 100);
};

const getStatusColor = (status: string): string => {
  switch (status?.toLowerCase()) {
    case 'approved': case 'accepted': return 'success';
    case 'pending': return 'warning';
    case 'expired': case 'rejected': return 'danger';
    case 'sent': return 'primary';
    case 'draft': return 'secondary';
    default: return 'info';
  }
};

const isExpired = (): boolean => {
  if (!quote.value?.valid_until) return false;
  return new Date(quote.value.valid_until) < new Date();
};

const isExpiringSoon = (): boolean => {
  if (!quote.value?.valid_until) return false;
  const validUntil = new Date(quote.value.valid_until);
  const threeDaysFromNow = new Date();
  threeDaysFromNow.setDate(threeDaysFromNow.getDate() + 3);
  return validUntil <= threeDaysFromNow && validUntil >= new Date();
};

const getValidityPeriod = (): string => {
  if (!quote.value?.created_on || !quote.value?.valid_until) return '30 days';
  
  const created = new Date(quote.value.created_on);
  const validUntil = new Date(quote.value.valid_until);
  const diffTime = Math.abs(validUntil.getTime() - created.getTime());
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  
  return `${diffDays} days`;
};

const getEstimatedFlightTime = (): string => {
  const distance = quote.value?.distance || 0;
  if (distance === 0) return 'TBD';
  
  // Estimate flight time based on average speed of 400 mph
  const hours = distance / 400;
  const flightHours = Math.floor(hours);
  const flightMinutes = Math.round((hours - flightHours) * 60);
  
  if (flightHours > 0) {
    return `${flightHours}h ${flightMinutes}m`;
  } else {
    return `${flightMinutes}m`;
  }
};

const convertToTrip = () => {
  Swal.fire({
    title: 'Convert to Trip',
    text: 'Are you sure you want to convert this quote to a trip booking?',
    icon: 'question',
    showCancelButton: true,
    confirmButtonText: 'Yes, convert it!',
    cancelButtonText: 'Cancel'
  }).then((result) => {
    if (result.isConfirmed) {
      // Here you would make the API call to convert the quote
      Swal.fire({
        title: 'Success!',
        text: 'Quote has been converted to a trip.',
        icon: 'success'
      }).then(() => {
        // Refresh the quote data or redirect to trip
        fetchQuote();
      });
    }
  });
};

const downloadQuote = () => {
  Swal.fire({
    title: 'Download Quote',
    text: 'Quote PDF download would be implemented here',
    icon: 'info'
  });
};

const viewPatient = () => {
  if (quote.value?.patient_id) {
    router.push(`/admin/contacts/patients/${quote.value.patient_id}`);
  }
};

onMounted(() => {
  fetchQuote();
});
</script>